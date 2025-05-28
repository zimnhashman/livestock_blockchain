// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  // 1. Get the contract factory
  const DataStorage = await ethers.getContractFactory("DataStorage");

  // 2. Deploy the contract (new syntax)
  console.log("Deploying DataStorage...");
  const contract = await DataStorage.deploy();

  // 3. Wait for deployment confirmation
  await contract.deploymentTransaction().wait();

  console.log(`DataStorage deployed to: ${await contract.getAddress()}`);

  // 4. Save the address for backend use
  const fs = require("fs");
  fs.writeFileSync("../backend/contract-address.txt", await contract.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });