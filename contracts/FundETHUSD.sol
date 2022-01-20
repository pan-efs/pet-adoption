// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract FundETHUSD {

    AggregatorV3Interface public priceFeed;

    //Events
    event Fund(uint256 _usdAmount, string message);

    
    /**
     * @notice Convert an amount of ETH to USD
     * @param _priceFeed The address of chainlink's data feed for a specific network
     */
    constructor(address _priceFeed)
        public 
        {
            priceFeed = AggregatorV3Interface(_priceFeed);
        }
    
    
    /**
     * @notice Get the version of the price data feed
     */
    function getVersion()
        public
        view 
        returns(uint256)
        {
            return priceFeed.version();
        }

    
    /**
     * @notice Get the current price of the pair (i.e. ETH/USD)
     */
    function getPrice()
        public
        view
        returns(uint256)
        {
            (, int256 price, , , ) = priceFeed.latestRoundData();

            return uint256(price * 10000000000);
        }
    
    
    /**
     * @notice Convert an ETH amount to USD
     * @param _eth The amount of ETH
     * @dev Multiply the price with ETH amount, then divide it by the decimals which is 1e18
     */
    function getConversionRate(uint256 _eth)
        public
        view
        returns(uint256)
        {
            uint256 price = getPrice();
            uint256 ethToUsd = (price * _eth) / 1000000000000000000;

            return ethToUsd;
        }

}