const { ethers, network } = require("hardhat");
const fs = require("fs");

const FERROFY_OWNER = "0x91b2Aef20c29d87d8dcc48191b30FbC1562aAaF0";

async function deployContract(label, contractName, args = []) {
    console.log(`--- Deploying ${label} ---`);
    const Factory = await ethers.getContractFactory(contractName);
    const Contract = await Factory.deploy(...args);
    await Contract.waitForDeployment();
    const Address = await Contract.getAddress();
    console.log(`OK ${label}: ${Address}\n`);
    return { Contract, Address };
}

async function requireOwnerDeployer() {
    const [Deployer] = await ethers.getSigners();
    if (!Deployer) {
        throw new Error("No deployer account configured. Set PRIVATE_KEY in .env before deploying.");
    }

    const Deployer_Address = await Deployer.getAddress();
    if (Deployer_Address.toLowerCase() !== FERROFY_OWNER.toLowerCase()) {
        throw new Error(`Deployer must be ${FERROFY_OWNER}. Current deployer: ${Deployer_Address}`);
    }

    return { Deployer, Deployer_Address };
}

async function main() {
    console.log("\n========================================");
    console.log("FerroFy Smart Contract Deployment");
    console.log("========================================\n");

    if (network.name === "sepolia" && !process.env.PRIVATE_KEY) {
        throw new Error("PRIVATE_KEY is required for Sepolia deployment.");
    }

    const { Deployer_Address } = await requireOwnerDeployer();
    const Balance = await ethers.provider.getBalance(Deployer_Address);
    const Network = await ethers.provider.getNetwork();

    console.log(`Deployer Address : ${Deployer_Address}`);
    console.log(`Deployer Balance : ${ethers.formatEther(Balance)} ETH`);
    console.log(`Network          : ${Network.name} (${Network.chainId})\n`);

    const Deployed = {};

    const Temperature = await deployContract("FerroFy Temperature Token", "FerroFyTemperatureToken");
    Deployed.TemperatureToken = Temperature.Address;

    const Humidity = await deployContract("FerroFy Humidity Token", "FerroFyHumidityToken");
    Deployed.HumidityToken = Humidity.Address;

    const Mq2 = await deployContract("FerroFy MQ2 Token", "FerroFyMQ2Token");
    Deployed.Mq2Token = Mq2.Address;

    const Rain = await deployContract("FerroFy Rain Token", "FerroFyRainToken");
    Deployed.RainToken = Rain.Address;

    const Inrf = await deployContract("INRf FerroFy Indian Rupee", "INRf_FerroFy_Indian_Rupee");
    Deployed.InrfToken = Inrf.Address;

    const Storage = await deployContract("FerroFy Sensor Storage", "FerroFySensorStorage", [
        Deployed.TemperatureToken,
        Deployed.HumidityToken,
        Deployed.Mq2Token,
        Deployed.RainToken,
        Deployed.InrfToken
    ]);
    Deployed.SensorStorage = Storage.Address;

    console.log("--- Authorizing SensorStorage as FFy minter ---");
    const Tx1 = await Temperature.Contract.setMinter(Deployed.SensorStorage, true);
    await Tx1.wait();
    console.log(`OK TemperatureToken.setMinter: ${Tx1.hash}`);

    const Tx2 = await Humidity.Contract.setMinter(Deployed.SensorStorage, true);
    await Tx2.wait();
    console.log(`OK HumidityToken.setMinter: ${Tx2.hash}`);

    const Tx3 = await Mq2.Contract.setMinter(Deployed.SensorStorage, true);
    await Tx3.wait();
    console.log(`OK MQ2Token.setMinter: ${Tx3.hash}`);

    const Tx4 = await Rain.Contract.setMinter(Deployed.SensorStorage, true);
    await Tx4.wait();
    console.log(`OK RainToken.setMinter: ${Tx4.hash}\n`);

    fs.writeFileSync("Deployed_Addresses.json", JSON.stringify(Deployed, null, 4));

    console.log("========================================");
    console.log("Deployment Complete");
    console.log("========================================");
    console.log(`Temperature Token : ${Deployed.TemperatureToken}`);
    console.log(`Humidity Token    : ${Deployed.HumidityToken}`);
    console.log(`MQ2 Token         : ${Deployed.Mq2Token}`);
    console.log(`Rain Token        : ${Deployed.RainToken}`);
    console.log(`INRf Token        : ${Deployed.InrfToken}`);
    console.log(`Sensor Storage    : ${Deployed.SensorStorage}`);
    console.log("Addresses saved to Deployed_Addresses.json");
    console.log("========================================\n");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
