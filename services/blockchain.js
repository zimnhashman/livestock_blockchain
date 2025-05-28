// services/blockchain.js
const { ethers } = require("ethers");

class BlockchainService {
  constructor() {
    this.provider = new ethers.providers.JsonRpcProvider("http://localhost:7545");
    this.wallet = new ethers.Wallet(
      "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80", // Ganache private key
      this.provider
    );
  }

  async initContract(contractAddress, abi) {
    this.contract = new ethers.Contract(contractAddress, abi, this.wallet);
  }

  async submitData(dataId, dataHash, geoHash) {
    const tx = await this.contract.submitData(dataId, dataHash, geoHash);
    return tx.wait();
  }
}

module.exports = new BlockchainService();