# Optional Hardhat blockchain anchor

VeriShield works without a chain because the backend always writes a local SHA-256 revision chain. This Hardhat contract mirrors the PPT's blockchain layer and can anchor final human-review events on a local EVM network.

```powershell
cd blockchain
npm install
npm run compile
```

Terminal 1:
```powershell
npm run node
```

Terminal 2:
```powershell
npm run deploy:local
```

Copy the contract address, plus a private key from the local Hardhat node, into `server/.env`:

```env
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_PRIVATE_KEY=0x...
```

Only SHA-256 document hashes, status and event hashes go on-chain. The original identity document and extracted PII remain encrypted off-chain.
