(function () {
    "use strict";

    const SEPOLIA_CHAIN_ID = "0xaa36a7";
    const SEPOLIA_CHAIN_ID_DECIMAL = 11155111;
    const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000";
    const DEPLOYMENT_FILES = ["New_Contracts.json", "Deployed_Addresses.json", "Developed_Addresses.json"];

    const DATA_ABI = [
        "function inrfToken() view returns (address)",
        "function totalData() view returns (uint256)",
        "function latestDataId() view returns (uint256)",
        "function rewardTokenAddresses() view returns (address temperature,address humidity,address mq2,address rain)",
        "function INRF_UPLOAD_FEE() view returns (uint256)",
        "function INRF_FETCH_FEE() view returns (uint256)",
        "function uploadData(int256 temperatureCenti,uint256 humidityCenti,uint256 mq2Centi,uint256 rainCenti) returns (uint256 dataId)",
        "function fetchData(uint256 dataId) returns (tuple(address uploader,int256 temperatureCenti,uint256 humidityCenti,uint256 mq2Centi,uint256 rainCenti,uint256 timestamp) data)",
        "function fetchTemperature(uint256 dataId) returns (int256 temperatureCenti)",
        "function fetchHumidity(uint256 dataId) returns (uint256 humidityCenti)",
        "function fetchMQ2(uint256 dataId) returns (uint256 mq2Centi)",
        "function fetchRain(uint256 dataId) returns (uint256 rainCenti)",
        "event DataUploaded(uint256 indexed dataId,address indexed uploader,uint256 timestamp)",
        "event DataFetched(uint256 indexed dataId,address indexed fetcher,uint8 indexed dataType,address uploader,int256 temperatureCenti,uint256 humidityCenti,uint256 mq2Centi,uint256 rainCenti,uint256 timestamp)"
    ];

    const ERC20_ABI = [
        "function decimals() view returns (uint8)",
        "function symbol() view returns (string)",
        "function balanceOf(address account) view returns (uint256)",
        "function allowance(address owner,address spender) view returns (uint256)",
        "function approve(address spender,uint256 amount) returns (bool)"
    ];

    const state = {
        ethereum: null,
        provider: null,
        signer: null,
        walletAddress: "",
        paymentToken: null,
        paymentTokenAddress: "",
        paymentDecimals: 2,
        paymentSymbol: "INRf",
        deployment: null
    };

    let els = {};

    function onReady(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback, { once: true });
            return;
        }

        callback();
    }

    onReady(init);

    function init() {
        els = {
            networkStatus: byId("Network_Status"),
            connectButton: byId("Connect_Button"),
            inrfTokenAddress: byId("INRf_Token_Address"),
            walletAddress: byId("Wallet_Address"),
            paymentBalance: byId("Payment_Balance"),
            paymentTokenAddress: byId("Payment_Token_Address"),
            walletStatus: byId("Wallet_Status"),
            contractAddress: byId("Contract_Address"),
            loadContractButton: byId("Load_Contract_Button"),
            refreshButton: byId("Refresh_Button"),
            latestIdButton: byId("Latest_Id_Button"),
            uploadFee: byId("Upload_Fee"),
            fetchFee: byId("Fetch_Fee"),
            totalData: byId("Total_Data"),
            rewardTokens: byId("Reward_Tokens"),
            contractStatus: byId("Contract_Status"),
            temperature: byId("Temperature_Input"),
            humidity: byId("Humidity_Input"),
            mq2: byId("MQ2_Input"),
            rain: byId("Rain_Input"),
            uploadButton: byId("Upload_Button"),
            uploadStatus: byId("Upload_Status"),
            fetchId: byId("Fetch_Id_Input"),
            fetchType: byId("Fetch_Type_Select"),
            fetchButton: byId("Fetch_Button"),
            resultTemperature: byId("Result_Temperature"),
            resultHumidity: byId("Result_Humidity"),
            resultMq2: byId("Result_MQ2"),
            resultRain: byId("Result_Rain"),
            resultDataId: byId("Result_Data_Id"),
            resultUploader: byId("Result_Uploader"),
            resultTimestamp: byId("Result_Timestamp"),
            resultTx: byId("Result_Tx"),
            fetchStatus: byId("Fetch_Status")
        };

        hydrateFromStorage();
        bindEvents();
        refreshPaymentTokenDisplay();
        loadDeploymentAddresses();
        detectMetaMask();
        checkExistingConnection();
    }

    function byId(id) {
        return document.getElementById(id);
    }

    function hydrateFromStorage() {
        if (els.contractAddress) els.contractAddress.value = localStorage.getItem("ferrofyDataContract") || "";
        if (els.inrfTokenAddress) els.inrfTokenAddress.value = localStorage.getItem("ferrofyInrfToken") || "";
    }

    function bindEvents() {
        if (els.connectButton) els.connectButton.addEventListener("click", () => connectWallet({ requestAccounts: true }));
        if (els.inrfTokenAddress) els.inrfTokenAddress.addEventListener("change", handleInrfAddressChanged);
        if (els.loadContractButton) els.loadContractButton.addEventListener("click", refreshContract);
        if (els.refreshButton) els.refreshButton.addEventListener("click", refreshContract);
        if (els.latestIdButton) els.latestIdButton.addEventListener("click", useLatestDataId);
        if (els.uploadButton) els.uploadButton.addEventListener("click", uploadData);
        if (els.fetchButton) els.fetchButton.addEventListener("click", fetchData);
    }

    async function loadDeploymentAddresses() {
        for (const file of DEPLOYMENT_FILES) {
            try {
                const response = await fetch(file, { cache: "no-store" });
                if (!response.ok) {
                    continue;
                }

                const deployment = normalizeDeployment(await response.json());
                state.deployment = deployment;
                applyDeployment(deployment);
                setStatus(els.contractStatus, `Loaded addresses from ${file}.`, "ok");
                return;
            } catch (error) {
                continue;
            }
        }

        if (!els.contractAddress.value.trim()) {
            setStatus(els.contractStatus, "No deployment address file found. Enter the data contract manually.", "");
        }
    }

    function normalizeDeployment(raw) {
        return {
            temperatureToken: raw.TemperatureToken || raw.Temperature || raw.TToken || "",
            humidityToken: raw.HumidityToken || raw.Humidity || raw.HToken || "",
            mq2Token: raw.Mq2Token || raw.MQ2Token || raw.MqToken || raw.MToken || "",
            rainToken: raw.RainToken || raw.Rain || raw.RToken || "",
            inrfToken: raw.INRfToken || raw.InrfToken || raw.INRFToken || raw.INRf || raw.INRF || "",
            sensorStorage: raw.SensorStorage || raw.FerroFySensorStorage || raw.DataContract || raw.Storage || ""
        };
    }

    function applyDeployment(deployment) {
        if (isAddress(deployment.sensorStorage)) {
            els.contractAddress.value = ethers.getAddress(deployment.sensorStorage);
            localStorage.setItem("ferrofyDataContract", els.contractAddress.value);
        }

        if (isAddress(deployment.inrfToken)) {
            els.inrfTokenAddress.value = ethers.getAddress(deployment.inrfToken);
            localStorage.setItem("ferrofyInrfToken", els.inrfTokenAddress.value);
        }

        renderRewardTokensFromDeployment(deployment);
        refreshPaymentTokenDisplay();
    }

    function renderRewardTokensFromDeployment(deployment) {
        const tokens = [
            ["TEMP", deployment.temperatureToken],
            ["HUM", deployment.humidityToken],
            ["MQ2", deployment.mq2Token],
            ["RAIN", deployment.rainToken]
        ];

        if (tokens.every(([, address]) => isAddress(address))) {
            els.rewardTokens.textContent = tokens
                .map(([label, address]) => `${label} ${shortAddress(ethers.getAddress(address))}`)
                .join(" | ");
        }
    }

    function detectMetaMask() {
        state.ethereum = getMetaMaskProvider();

        if (!state.ethereum) {
            setStatus(els.walletStatus, "MetaMask is not detected in this browser.", "error");
            els.connectButton.disabled = true;
            return;
        }

        els.connectButton.disabled = false;
        els.connectButton.textContent = "Connect MetaMask";
        setStatus(els.walletStatus, "MetaMask ready.", "");

        state.ethereum.on("accountsChanged", handleAccountsChanged);
        state.ethereum.on("chainChanged", handleChainChanged);
    }

    function getMetaMaskProvider() {
        const ethereum = window.ethereum;
        if (!ethereum) {
            return null;
        }

        if (Array.isArray(ethereum.providers)) {
            return ethereum.providers.find((provider) => provider && provider.isMetaMask) || null;
        }

        return ethereum.isMetaMask ? ethereum : null;
    }

    async function checkExistingConnection() {
        if (!state.ethereum || !window.ethers) {
            return;
        }

        try {
            const accounts = await state.ethereum.request({ method: "eth_accounts" });
            if (accounts.length > 0) {
                await connectWallet({ requestAccounts: false });
            }
        } catch (error) {
            setStatus(els.walletStatus, friendlyError(error), "error");
        }
    }

    async function connectWallet({ requestAccounts }) {
        try {
            if (!window.ethers) {
                throw new Error("Ethers failed to load. Check the internet connection for the CDN script.");
            }

            if (!state.ethereum) {
                detectMetaMask();
            }
            if (!state.ethereum) {
                throw new Error("Install or enable MetaMask, then reload this page.");
            }

            els.connectButton.disabled = true;
            setStatus(els.walletStatus, requestAccounts ? "Opening MetaMask." : "Restoring MetaMask session.", "");

            const accounts = requestAccounts
                ? await state.ethereum.request({ method: "eth_requestAccounts" })
                : await state.ethereum.request({ method: "eth_accounts" });

            if (!accounts || accounts.length === 0) {
                throw new Error("No MetaMask account selected.");
            }

            await ensureSepolia();
            state.provider = new ethers.BrowserProvider(state.ethereum);
            state.signer = await state.provider.getSigner();
            state.walletAddress = await state.signer.getAddress();

            els.walletAddress.textContent = state.walletAddress;
            els.networkStatus.textContent = "Sepolia";
            els.connectButton.textContent = shortAddress(state.walletAddress);

            await syncPaymentToken();
            setStatus(els.walletStatus, `Connected: ${shortAddress(state.walletAddress)}`, "ok");
            await refreshContract();
        } catch (error) {
            setStatus(els.walletStatus, friendlyError(error), "error");
        } finally {
            els.connectButton.disabled = false;
        }
    }

    async function ensureSepolia() {
        const chainId = await state.ethereum.request({ method: "eth_chainId" });
        if (chainId === SEPOLIA_CHAIN_ID) {
            return;
        }

        try {
            await state.ethereum.request({
                method: "wallet_switchEthereumChain",
                params: [{ chainId: SEPOLIA_CHAIN_ID }]
            });
        } catch (error) {
            if (Number(error.code) !== 4902) {
                throw error;
            }

            await state.ethereum.request({
                method: "wallet_addEthereumChain",
                params: [
                    {
                        chainId: SEPOLIA_CHAIN_ID,
                        chainName: "Sepolia",
                        nativeCurrency: { name: "Sepolia Ether", symbol: "ETH", decimals: 18 },
                        rpcUrls: ["https://ethereum-sepolia-rpc.publicnode.com"],
                        blockExplorerUrls: ["https://sepolia.etherscan.io"]
                    }
                ]
            });
        }
    }

    async function handleAccountsChanged(accounts) {
        if (!accounts || accounts.length === 0) {
            resetWallet();
            setStatus(els.walletStatus, "MetaMask disconnected.", "");
            return;
        }

        await connectWallet({ requestAccounts: false });
    }

    function handleChainChanged(chainId) {
        if (chainId !== SEPOLIA_CHAIN_ID) {
            resetWallet();
            els.networkStatus.textContent = `Wrong network: ${Number(chainId).toString()}`;
            setStatus(els.walletStatus, "Switch MetaMask to Sepolia.", "error");
            return;
        }

        connectWallet({ requestAccounts: false });
    }

    function resetWallet() {
        state.provider = null;
        state.signer = null;
        state.walletAddress = "";
        state.paymentToken = null;
        els.walletAddress.textContent = "Not connected";
        els.paymentBalance.textContent = "-";
        els.connectButton.textContent = "Connect MetaMask";
    }

    async function handleInrfAddressChanged() {
        const addr = els.inrfTokenAddress.value.trim();
        if (addr) {
            localStorage.setItem("ferrofyInrfToken", addr);
        }

        refreshPaymentTokenDisplay();

        try {
            await syncPaymentToken();
            await refreshContract();
        } catch (error) {
            setStatus(els.walletStatus, friendlyError(error), "error");
        }
    }

    function getInrfAddress(allowEmpty) {
        const address = els.inrfTokenAddress.value.trim();
        if (!address) {
            if (allowEmpty) {
                return "";
            }
            throw new Error("Enter the INRf token address.");
        }
        if (!isAddress(address)) {
            throw new Error("Enter a valid INRf token address.");
        }

        return ethers.getAddress(address);
    }

    function refreshPaymentTokenDisplay() {
        const address = getInrfAddress(true) || "INRf address required";
        if (els.paymentTokenAddress) {
            els.paymentTokenAddress.textContent = address;
        }
        state.paymentTokenAddress = address === "INRf address required" ? "" : address;
    }

    async function syncPaymentToken() {
        refreshPaymentTokenDisplay();

        if (!state.signer || !state.paymentTokenAddress) {
            state.paymentToken = null;
            els.paymentBalance.textContent = "-";
            return;
        }

        state.paymentToken = new ethers.Contract(state.paymentTokenAddress, ERC20_ABI, state.signer);

        try {
            state.paymentDecimals = Number(await state.paymentToken.decimals());
            state.paymentSymbol = await state.paymentToken.symbol();
        } catch (error) {
            state.paymentDecimals = 2;
            state.paymentSymbol = "INRf";
        }

        await refreshBalance();
    }

    async function refreshBalance() {
        if (!state.paymentToken || !state.walletAddress) {
            return;
        }

        const balance = await state.paymentToken.balanceOf(state.walletAddress);
        els.paymentBalance.textContent = formatUnits(balance, state.paymentDecimals, state.paymentSymbol);
    }

    function getContractAddress() {
        const address = els.contractAddress.value.trim();
        if (!isAddress(address)) {
            throw new Error("Enter a valid data contract address.");
        }

        const checksum = ethers.getAddress(address);
        localStorage.setItem("ferrofyDataContract", checksum);
        return checksum;
    }

    function getDataContract() {
        if (!state.signer) {
            throw new Error("Connect MetaMask first.");
        }

        return new ethers.Contract(getContractAddress(), DATA_ABI, state.signer);
    }

    async function refreshContract() {
        try {
            if (!state.signer) {
                setStatus(els.contractStatus, "Connect MetaMask to load contract data.", "");
                return;
            }

            const dataContract = getDataContract();
            const [totalData, rewardTokens, contractInrf, uploadFee, fetchFee] = await Promise.all([
                dataContract.totalData(),
                dataContract.rewardTokenAddresses(),
                dataContract.inrfToken(),
                dataContract.INRF_UPLOAD_FEE(),
                dataContract.INRF_FETCH_FEE()
            ]);

            if (contractInrf && contractInrf !== ZERO_ADDRESS && !els.inrfTokenAddress.value.trim()) {
                els.inrfTokenAddress.value = contractInrf;
                localStorage.setItem("ferrofyInrfToken", contractInrf);
                refreshPaymentTokenDisplay();
            }

            const temperatureToken = rewardTokens.temperature || rewardTokens[0];
            const humidityToken = rewardTokens.humidity || rewardTokens[1];
            const mq2Token = rewardTokens.mq2 || rewardTokens[2];
            const rainToken = rewardTokens.rain || rewardTokens[3];

            els.totalData.textContent = totalData.toString();
            els.rewardTokens.textContent =
                `TEMP ${shortAddress(temperatureToken)} | HUM ${shortAddress(humidityToken)} | ` +
                `MQ2 ${shortAddress(mq2Token)} | RAIN ${shortAddress(rainToken)}`;

            await syncPaymentToken();

            els.uploadFee.textContent = formatUnits(uploadFee, state.paymentDecimals, state.paymentSymbol);
            els.fetchFee.textContent = formatUnits(fetchFee, state.paymentDecimals, state.paymentSymbol);

            setStatus(els.contractStatus, "Contract loaded.", "ok");
        } catch (error) {
            setStatus(els.contractStatus, friendlyError(error), "error");
        }
    }

    async function useLatestDataId() {
        try {
            const dataContract = getDataContract();
            const latestId = await dataContract.latestDataId();
            els.fetchId.value = latestId.toString();
            setStatus(els.contractStatus, "Latest data ID loaded.", "ok");
        } catch (error) {
            setStatus(els.contractStatus, friendlyError(error), "error");
        }
    }

    async function approveIfNeeded(spender, amount) {
        await syncPaymentToken();
        if (!state.paymentToken) {
            throw new Error("Enter the INRf token address first.");
        }

        const allowance = await state.paymentToken.allowance(state.walletAddress, spender);
        if (allowance >= amount) {
            return;
        }

        setStatus(els.walletStatus, `Approving ${formatUnits(amount, state.paymentDecimals, state.paymentSymbol)}.`, "");
        const approveTx = await state.paymentToken.approve(spender, amount);
        await approveTx.wait();
        await refreshBalance();
    }

    async function uploadData() {
        try {
            els.uploadButton.disabled = true;
            const dataContract = getDataContract();
            const contractAddress = await dataContract.getAddress();
            const uploadFee = await dataContract.INRF_UPLOAD_FEE();

            const temperature = requireIntegerInput(els.temperature, -5500, 12500);
            const humidity = requireIntegerInput(els.humidity, 0, 10000);
            const mq2 = requireIntegerInput(els.mq2, 0, 102300);
            const rain = requireIntegerInput(els.rain, 0, 102300);

            await approveIfNeeded(contractAddress, uploadFee);
            setStatus(els.uploadStatus, "Uploading data.", "");

            const tx = await dataContract.uploadData(temperature, humidity, mq2, rain);
            const receipt = await tx.wait();
            const uploaded = findEvent(dataContract, receipt, "DataUploaded");

            if (uploaded) {
                els.fetchId.value = uploaded.args.dataId.toString();
                els.resultDataId.textContent = uploaded.args.dataId.toString();
                els.resultUploader.textContent = uploaded.args.uploader;
                els.resultTimestamp.textContent = formatTimestamp(uploaded.args.timestamp);
            }

            els.resultTemperature.textContent = centiToText(BigInt(temperature), " °C");
            els.resultHumidity.textContent = centiToText(BigInt(humidity), "%");
            els.resultMq2.textContent = centiToText(BigInt(mq2), "");
            els.resultRain.textContent = centiToText(BigInt(rain), "");
            els.resultTx.textContent = receipt.hash;

            setStatus(els.uploadStatus, `Upload confirmed: ${receipt.hash}`, "ok");
            await refreshBalance();
            await refreshContract();
        } catch (error) {
            setStatus(els.uploadStatus, friendlyError(error), "error");
        } finally {
            els.uploadButton.disabled = false;
        }
    }

    async function fetchData() {
        try {
            els.fetchButton.disabled = true;
            const dataContract = getDataContract();
            const contractAddress = await dataContract.getAddress();
            const fetchFee = await dataContract.INRF_FETCH_FEE();
            const dataId = requireIntegerInput(els.fetchId, 0, Number.MAX_SAFE_INTEGER);
            const fetchType = els.fetchType.value;

            await approveIfNeeded(contractAddress, fetchFee);
            setStatus(els.fetchStatus, "Fetching data.", "");

            let tx;
            if (fetchType === "temperature") {
                tx = await dataContract.fetchTemperature(dataId);
            } else if (fetchType === "humidity") {
                tx = await dataContract.fetchHumidity(dataId);
            } else if (fetchType === "mq2") {
                tx = await dataContract.fetchMQ2(dataId);
            } else if (fetchType === "rain") {
                tx = await dataContract.fetchRain(dataId);
            } else {
                tx = await dataContract.fetchData(dataId);
            }

            const receipt = await tx.wait();
            const fetched = findEvent(dataContract, receipt, "DataFetched");
            if (!fetched) {
                throw new Error("Fetch event not found.");
            }

            renderFetchedResult(fetched.args, receipt.hash);
            setStatus(els.fetchStatus, `Fetch confirmed: ${receipt.hash}`, "ok");
            await refreshBalance();
            await refreshContract();
        } catch (error) {
            setStatus(els.fetchStatus, friendlyError(error), "error");
        } finally {
            els.fetchButton.disabled = false;
        }
    }

    function findEvent(contract, receipt, name) {
        for (const log of receipt.logs) {
            try {
                const parsed = contract.interface.parseLog(log);
                if (parsed && parsed.name === name) {
                    return parsed;
                }
            } catch (error) {
                continue;
            }
        }

        return null;
    }

    function renderFetchedResult(args, txHash) {
        const dataType = Number(args.dataType);

        els.resultDataId.textContent = args.dataId.toString();
        els.resultUploader.textContent = args.uploader;
        els.resultTimestamp.textContent = formatTimestamp(args.timestamp);
        els.resultTx.textContent = txHash;

        if (dataType === 0 || dataType === 1) {
            els.resultTemperature.textContent = centiToText(args.temperatureCenti, " °C");
        }
        if (dataType === 0 || dataType === 2) {
            els.resultHumidity.textContent = centiToText(args.humidityCenti, "%");
        }
        if (dataType === 0 || dataType === 3) {
            els.resultMq2.textContent = centiToText(args.mq2Centi, "");
        }
        if (dataType === 0 || dataType === 4) {
            els.resultRain.textContent = centiToText(args.rainCenti, "");
        }
    }

    function setStatus(element, message, kind) {
        element.textContent = message;
        element.classList.remove("ok", "error");
        if (kind) {
            element.classList.add(kind);
        }
    }

    function shortAddress(address) {
        if (!address || address.length < 12) {
            return address || "-";
        }

        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }

    function formatUnits(value, decimals, symbol) {
        return `${ethers.formatUnits(value, decimals)} ${symbol}`;
    }

    function centiToText(value, suffix) {
        let amount = BigInt(value);
        const sign = amount < 0n ? "-" : "";
        if (amount < 0n) {
            amount = -amount;
        }

        const whole = amount / 100n;
        const fraction = String(amount % 100n).padStart(2, "0");
        return `${sign}${whole}.${fraction}${suffix}`;
    }

    function requireIntegerInput(input, min, max) {
        const value = Number(input.value);
        if (!Number.isInteger(value) || value < min || value > max) {
            throw new Error(`${input.previousElementSibling.textContent} is out of range.`);
        }

        return value;
    }

    function formatTimestamp(value) {
        const seconds = Number(value);
        if (!Number.isFinite(seconds) || seconds <= 0) {
            return "-";
        }

        return new Date(seconds * 1000).toLocaleString();
    }

    function isAddress(value) {
        return Boolean(window.ethers && value && ethers.isAddress(value));
    }

    function friendlyError(error) {
        if (!error) {
            return "Unknown error.";
        }

        if (error.code === 4001 || error.code === "ACTION_REJECTED") {
            return "Request rejected in MetaMask.";
        }
        if (error.code === -32002) {
            return "MetaMask already has a pending request. Open MetaMask to continue.";
        }
        if (error.info && error.info.error && error.info.error.message) {
            return error.info.error.message;
        }
        if (error.shortMessage) {
            return error.shortMessage;
        }
        if (error.reason) {
            return error.reason;
        }
        if (error.message) {
            return error.message;
        }

        return String(error);
    }

    window.FerroFyMetaMask = {
        connectWallet: () => connectWallet({ requestAccounts: true }),
        refreshContract,
        get state() {
            return {
                walletAddress: state.walletAddress,
                paymentTokenAddress: state.paymentTokenAddress,
                deployment: state.deployment,
                chainId: SEPOLIA_CHAIN_ID_DECIMAL
            };
        }
    };
})();
