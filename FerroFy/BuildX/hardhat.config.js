require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const DEFAULT_SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com";
const Private_Key = process.env.PRIVATE_KEY ? process.env.PRIVATE_KEY.trim() : "";
const Rpc_Url = process.env.RPC_URL || DEFAULT_SEPOLIA_RPC_URL;
const Etherscan_Api_Key = process.env.ETHERSCAN_API_KEY || "";

function getAccounts() {
    if (!Private_Key) {
        return [];
    }

    return [Private_Key.startsWith("0x") ? Private_Key : `0x${Private_Key}`];
}

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: {
        version: "0.8.20",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200
            }
        }
    },
    networks: {
        hardhat: {},
        localhost: {
            url: "http://127.0.0.1:8545"
        },
        sepolia: {
            url: Rpc_Url,
            accounts: getAccounts(),
            chainId: 11155111
        }
    },
    etherscan: {
        apiKey: Etherscan_Api_Key
    },
    paths: {
        sources: "./Contracts",
        tests: "./test",
        cache: "./cache",
        artifacts: "./artifacts"
    }
};
