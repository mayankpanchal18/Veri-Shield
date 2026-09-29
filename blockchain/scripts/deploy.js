import hre from 'hardhat';

const registry = await hre.ethers.deployContract('VeriShieldRegistry');
await registry.waitForDeployment();
console.log('VeriShieldRegistry:', await registry.getAddress());
console.log('Put this address into server/.env as BLOCKCHAIN_CONTRACT_ADDRESS.');
