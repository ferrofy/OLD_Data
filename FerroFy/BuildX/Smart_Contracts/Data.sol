// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20Payment {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

interface IFFyRewardToken {
    function mint(address to, uint256 amount) external;
}

contract FerroFySensorStorage {
    address public constant FERROFY_OWNER = 0x91b2Aef20c29d87d8dcc48191b30FbC1562aAaF0;
    address public constant NODE_1 = 0x6db68d2801fc725630Ed4E0959250987031D3954;
    address public constant NODE_2 = 0x48dEb715e1CfCc8684B6C198F162177f49621cb2;
    address public constant TESTNET_USD_TOKEN = 0xCaC524BcA292aaade2DF8A05cC58F0a65B1B3bB9;

    uint256 public constant TESTNET_USD_UPLOAD_FEE = 500_000;
    uint256 public constant TESTNET_USD_FETCH_FEE = 250_000;
    uint256 public constant INRF_UPLOAD_FEE = 50;
    uint256 public constant INRF_FETCH_FEE = 25;
    uint256 public constant REWARD_AMOUNT = 1 ether;

    uint8 private constant REWARD_ALL = 0;
    uint8 private constant REWARD_TEMPERATURE = 1;
    uint8 private constant REWARD_HUMIDITY = 2;
    uint8 private constant REWARD_MQ2 = 3;
    uint8 private constant REWARD_RAIN = 4;

    address public temperatureToken;
    address public humidityToken;
    address public mq2Token;
    address public rainToken;
    address public inrfToken;

    mapping(address => bool) public dataNodes;

    struct PaymentTokenConfig {
        bool enabled;
        uint256 uploadFee;
        uint256 fetchFee;
    }

    mapping(address => PaymentTokenConfig) private paymentTokenConfigs;

    struct SensorData {
        address uploader;
        int256 temperatureCentiCelsius;
        uint256 humidityCentiPercent;
        uint256 mq2Reading;
        uint256 rainReading;
        uint256 timestamp;
    }

    SensorData[] private sensorData;
    uint256 private reentryLock = 1;

    event DataNodeUpdated(address indexed node, bool allowed);
    event RewardTokensUpdated(
        address indexed temperatureToken,
        address indexed humidityToken,
        address indexed mq2Token,
        address rainToken
    );
    event INRfTokenUpdated(address indexed token);
    event PaymentTokenUpdated(address indexed token, bool enabled, uint256 uploadFee, uint256 fetchFee);
    event PaymentCollected(address indexed payer, address indexed token, uint256 amount, uint8 indexed paymentType);
    event DataUploaded(uint256 indexed dataId, address indexed uploader, address indexed paymentToken, uint256 timestamp);
    event DataFetched(
        uint256 indexed dataId,
        address indexed fetcher,
        uint8 indexed dataType,
        address paymentToken,
        address uploader,
        int256 temperatureCentiCelsius,
        uint256 humidityCentiPercent,
        uint256 mq2Reading,
        uint256 rainReading,
        uint256 timestamp
    );
    event RewardMinted(address indexed account, address indexed token, uint256 amount, uint8 indexed dataType);

    modifier onlyOwner() {
        require(msg.sender == FERROFY_OWNER, "Only FerroFy owner");
        _;
    }

    modifier onlyDataNode() {
        require(dataNodes[msg.sender], "Only approved data node");
        _;
    }

    modifier nonReentrant() {
        require(reentryLock == 1, "Reentrant call");
        reentryLock = 2;
        _;
        reentryLock = 1;
    }

    constructor(
        address temperatureToken_,
        address humidityToken_,
        address mq2Token_,
        address rainToken_,
        address inrfToken_
    ) {
        require(msg.sender == FERROFY_OWNER, "Deploy from FerroFy owner");

        _setRewardTokens(temperatureToken_, humidityToken_, mq2Token_, rainToken_);
        _setDataNode(FERROFY_OWNER, true);
        _setDataNode(NODE_1, true);
        _setDataNode(NODE_2, true);
        _setPaymentToken(TESTNET_USD_TOKEN, true, TESTNET_USD_UPLOAD_FEE, TESTNET_USD_FETCH_FEE);

        if (inrfToken_ != address(0)) {
            inrfToken = inrfToken_;
            emit INRfTokenUpdated(inrfToken_);
            _setPaymentToken(inrfToken_, true, INRF_UPLOAD_FEE, INRF_FETCH_FEE);
        }
    }

    function setDataNode(address node, bool allowed) external onlyOwner {
        require(node != address(0), "Invalid node");

        _setDataNode(node, allowed);
    }

    function setRewardTokens(
        address temperatureToken_,
        address humidityToken_,
        address mq2Token_,
        address rainToken_
    ) external onlyOwner {
        _setRewardTokens(temperatureToken_, humidityToken_, mq2Token_, rainToken_);
    }

    function setINRfToken(address token, uint256 uploadFee, uint256 fetchFee) external onlyOwner {
        require(token != address(0), "Invalid INRf token");

        inrfToken = token;
        emit INRfTokenUpdated(token);
        _setPaymentToken(token, true, uploadFee, fetchFee);
    }

    function setPaymentToken(address token, bool enabled, uint256 uploadFee, uint256 fetchFee) external onlyOwner {
        _setPaymentToken(token, enabled, uploadFee, fetchFee);
    }

    function uploadData(
        address paymentToken,
        int256 temperatureCentiCelsius,
        uint256 humidityCentiPercent,
        uint256 mq2Reading,
        uint256 rainReading
    ) external onlyDataNode nonReentrant returns (uint256 dataId) {
        _validateSensorData(temperatureCentiCelsius, humidityCentiPercent, mq2Reading, rainReading);
        _collectPayment(paymentToken, true);

        sensorData.push(
            SensorData({
                uploader: msg.sender,
                temperatureCentiCelsius: temperatureCentiCelsius,
                humidityCentiPercent: humidityCentiPercent,
                mq2Reading: mq2Reading,
                rainReading: rainReading,
                timestamp: block.timestamp
            })
        );

        dataId = sensorData.length - 1;
        _mintAllRewards(msg.sender);

        emit DataUploaded(dataId, msg.sender, paymentToken, block.timestamp);
    }

    function fetchData(address paymentToken, uint256 dataId) external nonReentrant returns (SensorData memory data) {
        data = _loadData(dataId);
        _collectPayment(paymentToken, false);
        _mintAllRewards(msg.sender);

        emit DataFetched(
            dataId,
            msg.sender,
            REWARD_ALL,
            paymentToken,
            data.uploader,
            data.temperatureCentiCelsius,
            data.humidityCentiPercent,
            data.mq2Reading,
            data.rainReading,
            data.timestamp
        );
    }

    function fetchTemperature(address paymentToken, uint256 dataId)
        external
        nonReentrant
        returns (int256 temperatureCentiCelsius)
    {
        SensorData memory data = _loadData(dataId);

        _collectPayment(paymentToken, false);
        _mintReward(temperatureToken, msg.sender, REWARD_TEMPERATURE);

        temperatureCentiCelsius = data.temperatureCentiCelsius;
        emit DataFetched(
            dataId,
            msg.sender,
            REWARD_TEMPERATURE,
            paymentToken,
            data.uploader,
            temperatureCentiCelsius,
            0,
            0,
            0,
            data.timestamp
        );
    }

    function fetchHumidity(address paymentToken, uint256 dataId) external nonReentrant returns (uint256 humidityCentiPercent) {
        SensorData memory data = _loadData(dataId);

        _collectPayment(paymentToken, false);
        _mintReward(humidityToken, msg.sender, REWARD_HUMIDITY);

        humidityCentiPercent = data.humidityCentiPercent;
        emit DataFetched(
            dataId,
            msg.sender,
            REWARD_HUMIDITY,
            paymentToken,
            data.uploader,
            0,
            humidityCentiPercent,
            0,
            0,
            data.timestamp
        );
    }

    function fetchMQ2(address paymentToken, uint256 dataId) external nonReentrant returns (uint256 mq2Reading) {
        SensorData memory data = _loadData(dataId);

        _collectPayment(paymentToken, false);
        _mintReward(mq2Token, msg.sender, REWARD_MQ2);

        mq2Reading = data.mq2Reading;
        emit DataFetched(
            dataId,
            msg.sender,
            REWARD_MQ2,
            paymentToken,
            data.uploader,
            0,
            0,
            mq2Reading,
            0,
            data.timestamp
        );
    }

    function fetchRain(address paymentToken, uint256 dataId) external nonReentrant returns (uint256 rainReading) {
        SensorData memory data = _loadData(dataId);

        _collectPayment(paymentToken, false);
        _mintReward(rainToken, msg.sender, REWARD_RAIN);

        rainReading = data.rainReading;
        emit DataFetched(
            dataId,
            msg.sender,
            REWARD_RAIN,
            paymentToken,
            data.uploader,
            0,
            0,
            0,
            rainReading,
            data.timestamp
        );
    }

    function totalData() external view returns (uint256) {
        return sensorData.length;
    }

    function latestDataId() external view returns (uint256) {
        require(sensorData.length > 0, "No data yet");

        return sensorData.length - 1;
    }

    function rewardTokenAddresses()
        external
        view
        returns (address temperature, address humidity, address mq2, address rain)
    {
        return (temperatureToken, humidityToken, mq2Token, rainToken);
    }

    function paymentTokenAddresses() external view returns (address testnetUsdToken, address inrToken) {
        return (TESTNET_USD_TOKEN, inrfToken);
    }

    function getPaymentFees(address token) external view returns (bool enabled, uint256 uploadFee, uint256 fetchFee) {
        PaymentTokenConfig memory config = paymentTokenConfigs[token];

        return (config.enabled, config.uploadFee, config.fetchFee);
    }

    function _setDataNode(address node, bool allowed) private {
        dataNodes[node] = allowed;

        emit DataNodeUpdated(node, allowed);
    }

    function _setRewardTokens(
        address temperatureToken_,
        address humidityToken_,
        address mq2Token_,
        address rainToken_
    ) private {
        require(temperatureToken_ != address(0), "Invalid temperature token");
        require(humidityToken_ != address(0), "Invalid humidity token");
        require(mq2Token_ != address(0), "Invalid MQ2 token");
        require(rainToken_ != address(0), "Invalid rain token");

        temperatureToken = temperatureToken_;
        humidityToken = humidityToken_;
        mq2Token = mq2Token_;
        rainToken = rainToken_;

        emit RewardTokensUpdated(temperatureToken_, humidityToken_, mq2Token_, rainToken_);
    }

    function _setPaymentToken(address token, bool enabled, uint256 uploadFee, uint256 fetchFee) private {
        require(token != address(0), "Invalid payment token");
        if (enabled) {
            require(uploadFee > 0, "Invalid upload fee");
            require(fetchFee > 0, "Invalid fetch fee");
        }

        paymentTokenConfigs[token] = PaymentTokenConfig({enabled: enabled, uploadFee: uploadFee, fetchFee: fetchFee});
        emit PaymentTokenUpdated(token, enabled, uploadFee, fetchFee);
    }

    function _validateSensorData(
        int256 temperatureCentiCelsius,
        uint256 humidityCentiPercent,
        uint256 mq2Reading,
        uint256 rainReading
    ) private pure {
        require(
            temperatureCentiCelsius >= -5500 && temperatureCentiCelsius <= 12500,
            "Temperature out of range"
        );
        require(humidityCentiPercent <= 10000, "Humidity out of range");
        require(mq2Reading <= 1023, "MQ2 out of range");
        require(rainReading <= 1023, "Rain out of range");
    }

    function _loadData(uint256 dataId) private view returns (SensorData memory data) {
        require(dataId < sensorData.length, "Data not found");

        data = sensorData[dataId];
    }

    function _collectPayment(address token, bool isUpload) private {
        PaymentTokenConfig memory config = paymentTokenConfigs[token];
        require(config.enabled, "Payment token disabled");
        require(token.code.length > 0, "Payment token missing");

        uint256 amount = isUpload ? config.uploadFee : config.fetchFee;
        uint8 paymentType = isUpload ? 1 : 2;

        (bool success, bytes memory returnData) = token.call(
            abi.encodeWithSelector(IERC20Payment.transferFrom.selector, msg.sender, FERROFY_OWNER, amount)
        );

        require(success, "Payment failed");

        if (returnData.length > 0) {
            require(abi.decode(returnData, (bool)), "Payment rejected");
        }

        emit PaymentCollected(msg.sender, token, amount, paymentType);
    }

    function _mintAllRewards(address account) private {
        _mintReward(temperatureToken, account, REWARD_TEMPERATURE);
        _mintReward(humidityToken, account, REWARD_HUMIDITY);
        _mintReward(mq2Token, account, REWARD_MQ2);
        _mintReward(rainToken, account, REWARD_RAIN);
    }

    function _mintReward(address token, address account, uint8 dataType) private {
        require(token.code.length > 0, "Reward token missing");
        IFFyRewardToken(token).mint(account, REWARD_AMOUNT);

        emit RewardMinted(account, token, REWARD_AMOUNT, dataType);
    }
}
