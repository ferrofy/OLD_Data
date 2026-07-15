// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./SensorTokenBase.sol";

contract FerroFy_HUM is SensorTokenBase {
    constructor() SensorTokenBase("Humidity", "HUM") {}
}
