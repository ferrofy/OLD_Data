// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./FFyRewardTokenBase.sol";

contract FerroFyTemperatureToken is FFyRewardTokenBase {
    constructor() FFyRewardTokenBase("FerroFy Temperature", "T") {}
}
