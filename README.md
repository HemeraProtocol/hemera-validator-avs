<h1>Hemera Validator AVS</h1>
<p>By Hemera Protocol</p>
<p></p>

> [!NOTE]
> The Hemera Validator AVS is a work-in-progress project. If you need to use it in production, please consult the Hemera Team first.

## About Hemera Protocol

Hemera Protocol is a decentralized, account-centric programmable indexing network created to function as a public goods data infrastructure, enhancing the capabilities of data networks in web3. This platform supports many web3 applications, from straightforward to intricate, such as blockchain explorers, on-chain asset portfolios, social graphs, zero-knowledge (ZK) coprocessors, community quality auditing, and web3 identities. All these can benefit from or be built on top of Hemera.

## About Hemera Validator AVS

Hemera Validators are node operators responsible for securing the network. The major responsibility of the validator is to validate responses provided by indexers.
This project demonstrates how a validator should work on top of the Othentic Stack and EigenLayer.

## Technical description

1. Task performer received a request to Hemera Indexing Network querying either a wallet address's transaction history or token holding.
2. Task performer submits the task to IPFS (Smart Contract).
3. Operators (Validators) receive the task and start to validate by querying their own source of data (rpc endpoints).
4. Operators validate the Hemera Network data response.

## Contract Deployed

The following addresses are now available for use:
L1:

- ERC20: 0x1144Cd27D171D953338471BEB866f2550bE709aA
- AvsGovernance: 0x5D7A993e0e4d3FDcF1Da2423bA8CB3961E9Bf5F6
- Vault: 0x5d0D016dDfFa75aa942f9827532FFa0C638A2620
- L1MessageHandler: 0xbB6b4D7E3B5Bf57108164d729bc926A18f8A9694 (1.0 ETH)

L2:

- AttestationCenter: 0x7ab99Cc3d43a538E23caB9F45773a60d45295618
- L2MessageHandler: 0x930287cb5F9bB7B1d1e8059a72f2960142D45F07 (2.0 ETH)
- OBLS: 0x1144Cd27D171D953338471BEB866f2550bE709aA
- BN256G2: 0x2D58f7dDc87238A1630A4E9f4AA2B04d4e08D359
  AVS deployment done!

OTHENTIC_REGISTRY_ADDRESS=0x41994741eD86Ec48e9578d0f64839E3F546466Fa
AVS_GOVERNANCE_ADDRESS=0x5D7A993e0e4d3FDcF1Da2423bA8CB3961E9Bf5F6
ATTESTATION_CENTER_ADDRESS=0x7ab99Cc3d43a538E23caB9F45773a60d45295618

ATTESTER1=0xFDEaCf567997fC153E2Fe1DE098aEEDC71294b71
ATTESTER2=0x9a245c07Dd43F65a80E4fA8DeAF1664C8A038109
ATTESTER3=0x3b5BBca213AEDB52f546eab1E9c9D881B5668c90
