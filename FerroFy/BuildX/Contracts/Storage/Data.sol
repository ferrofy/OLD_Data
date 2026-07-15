// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20Payment {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

interface ISensorToken {
    function mint(address to, uint256 amount) external;
}

contract FerroFySensorStorage {
    address public constant FERROFY_OWNER = 0x91b2Aef20c29d87d8dcc48191b30FbC1562aAaF0;
    address public constant NODE_1 = 0x6db68d2801fc725630Ed4E0959250987031D3954;
    address public constant NODE_2 = 0x48dEb715e1CfCc8684B6C198F162177f49621cb2;

    uint256 public constant INRF_UPLOAD_FEE = 50;
    uint256 public constant INRF_FETCH_FEE = 25;

    address public temperatureToken;
    address public humidityToken;
    address public mq2Token;
    address public rainToken;
    address public inrfToken;

    mapping(address => bool) public dataNodes;

    struct SensorData {
        address uploader;
        int256 temperatureCenti;
        uint256 humidityCenti;
        uint256 mq2Centi;
        uint256 rainCenti;
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
    event DataUploaded(uint256 indexed dataId, address indexed uploader, uint256 timestamp);
    event DataFetched(
        uint256 indexed dataId,
        address indexed fetcher,
        uint8 indexed dataType,
        address uploader,
        int256 temperatureCenti,
        uint256 humidityCenti,
        uint256 mq2Centi,
        uint256 rainCenti,
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
        require(inrfToken_ != address(0), "Invalid INRf token");
        inrfToken = inrfToken_;
        emit INRfTokenUpdated(inrfToken_);
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

    function setINRfToken(address token) external onlyOwner {
        require(token != address(0), "Invalid INRf token");
        inrfToken = token;
        emit INRfTokenUpdated(token);
    }

    function uploadData(
        int256 temperatureCenti,
        uint256 humidityCenti,
        uint256 mq2Centi,
        uint256 rainCenti
    ) external onlyDataNode nonReentrant returns (uint256 dataId) {
        _validateSensorData(temperatureCenti, humidityCenti, mq2Centi, rainCenti);
        _collectPayment(true);

        sensorData.push(
            SensorData({
                uploader: msg.sender,
                temperatureCenti: temperatureCenti,
                humidityCenti: humidityCenti,
                mq2Centi: mq2Centi,
                rainCenti: rainCenti,
                timestamp: block.timestamp
            })
        );

        dataId = sensorData.length - 1;
        _mintSensorRewards(msg.sender, temperatureCenti, humidityCenti, mq2Centi, rainCenti);

        emit DataUploaded(dataId, msg.sender, block.timestamp);
    }

    function fetchData(uint256 dataId) external nonReentrant returns (SensorData memory data) {
        data = _loadData(dataId);
        _collectPayment(false);
        _mintSensorRewards(msg.sender, data.temperatureCenti, data.humidityCenti, data.mq2Centi, data.rainCenti);

        emit DataFetched(
            dataId,
            msg.sender,
            0,
            data.uploader,
            data.temperatureCenti,
            data.humidityCenti,
            data.mq2Centi,
            data.rainCenti,
            data.timestamp
        );
    }

    function fetchTemperature(uint256 dataId) external nonReentrant returns (int256 temperatureCenti) {
        SensorData memory data = _loadData(dataId);
        _collectPayment(false);

        uint256 rewardAmount = data.temperatureCenti >= 0 ? uint256(data.temperatureCenti) : uint256(-data.temperatureCenti);
        if (rewardAmount > 0) {
            _mintReward(temperatureToken, msg.sender, rewardAmount, 1);
        }

        temperatureCenti = data.temperatureCenti;
        emit DataFetched(dataId, msg.sender, 1, data.uploader, temperatureCenti, 0, 0, 0, data.timestamp);
    }

    function fetchHumidity(uint256 dataId) external nonReentrant returns (uint256 humidityCenti) {
        SensorData memory data = _loadData(dataId);
        _collectPayment(false);

        if (data.humidityCenti > 0) {
            _mintReward(humidityToken, msg.sender, data.humidityCenti, 2);
        }

        humidityCenti = data.humidityCenti;
        emit DataFetched(dataId, msg.sender, 2, data.uploader, 0, humidityCenti, 0, 0, data.timestamp);
    }

    function fetchMQ2(uint256 dataId) external nonReentrant returns (uint256 mq2Centi) {
        SensorData memory data = _loadData(dataId);
        _collectPayment(false);

        if (data.mq2Centi > 0) {
            _mintReward(mq2Token, msg.sender, data.mq2Centi, 3);
        }

        mq2Centi = data.mq2Centi;
        emit DataFetched(dataId, msg.sender, 3, data.uploader, 0, 0, mq2Centi, 0, data.timestamp);
    }

    function fetchRain(uint256 dataId) external nonReentrant returns (uint256 rainCenti) {
        SensorData memory data = _loadData(dataId);
        _collectPayment(false);

        if (data.rainCenti > 0) {
            _mintReward(rainToken, msg.sender, data.rainCenti, 4);
        }

        rainCenti = data.rainCenti;
        emit DataFetched(dataId, msg.sender, 4, data.uploader, 0, 0, 0, rainCenti, data.timestamp);
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

    function _validateSensorData(
        int256 temperatureCenti,
        uint256 humidityCenti,
        uint256 mq2Centi,
        uint256 rainCenti
    ) private pure {
        require(temperatureCenti >= -5500 && temperatureCenti <= 12500, "Temperature out of range");
        require(humidityCenti <= 10000, "Humidity out of range");
        require(mq2Centi <= 102300, "MQ2 out of range");
        require(rainCenti <= 102300, "Rain out of range");
    }

    function _loadData(uint256 dataId) private view returns (SensorData memory data) {
        require(dataId < sensorData.length, "Data not found");
        data = sensorData[dataId];
    }

    function _collectPayment(bool isUpload) private {
        require(inrfToken != address(0), "INRf token not set");
        require(inrfToken.code.length > 0, "INRf token missing");

        uint256 amount = isUpload ? INRF_UPLOAD_FEE : INRF_FETCH_FEE;

        (bool success, bytes memory returnData) = inrfToken.call(
            abi.encodeWithSelector(IERC20Payment.transferFrom.selector, msg.sender, FERROFY_OWNER, amount)
        );

        require(success, "Payment failed");

        if (returnData.length > 0) {
            require(abi.decode(returnData, (bool)), "Payment rejected");
        }
    }

    function _mintSensorRewards(
        address account,
        int256 temperatureCenti,
        uint256 humidityCenti,
        uint256 mq2Centi,
        uint256 rainCenti
    ) private {
        uint256 tempReward = temperatureCenti >= 0 ? uint256(temperatureCenti) : uint256(-temperatureCenti);
        if (tempReward > 0) {
            _mintReward(temperatureToken, account, tempReward, 1);
        }
        if (humidityCenti > 0) {
            _mintReward(humidityToken, account, humidityCenti, 2);
        }
        if (mq2Centi > 0) {
            _mintReward(mq2Token, account, mq2Centi, 3);
        }
        if (rainCenti > 0) {
            _mintReward(rainToken, account, rainCenti, 4);
        }
    }

    function _mintReward(address token, address account, uint256 amount, uint8 dataType) private {
        require(token.code.length > 0, "Reward token missing");
        ISensorToken(token).mint(account, amount);
        emit RewardMinted(account, token, amount, dataType);
    }
}
