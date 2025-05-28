const { ethers } = require("hardhat");

async function main() {
  const [sender, receiver] = await ethers.getSigners();

  console.log("Account 0:", sender.address);
  console.log("Account 1:", receiver.address);

  const tx = await sender.sendTransaction({
    to: receiver.address,
    value: ethers.parseEther("1.0"), // Send 1 ETH
  });

  console.log("Transaction hash:", tx.hash);
  await tx.wait();
  console.log("Transaction confirmed.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
