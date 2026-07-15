// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./FFyRewardTokenBase.sol";

contract FerroFyHumidityToken is FFyRewardTokenBase {
    constructor() FFyRewardTokenBase("FerroFy Humidity", "H") {}
}
