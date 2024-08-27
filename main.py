from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import random
from web3 import Web3

app = FastAPI()

# Web3 setup
INFURA_URL = "https://mainnet.infura.io/v3/df3f19c8bd6c4923ad40dcde5a12cc39"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
        <head>
            <title>Ethereum Mining WebApp</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Welcome to Ethereum Mining WebApp</h1>
            <button id="connectButton">Connect MetaMask Wallet</button>

            <script src="https://cdn.jsdelivr.net/npm/web3/dist/web3.min.js"></script>
            <script>
                let web3;

                async function connectMetaMask() {
                    if (typeof window.ethereum !== 'undefined' || typeof window.web3 !== 'undefined') {
                        // Modern dapp browsers...
                        web3 = new Web3(window['ethereum'] || window.web3.currentProvider);
                        try {
                            await ethereum.request({ method: 'eth_requestAccounts' });
                            const accounts = await web3.eth.getAccounts();
                            const walletAddress = accounts[0];
                            connectWallet(walletAddress);
                        } catch (error) {
                            console.error("User denied account access");
                        }
                    } else {
                        alert('MetaMask is not installed!');
                    }
                }

                async function connectWallet(walletAddress) {
                    const response = await fetch('/connect_wallet', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: `wallet_address=${walletAddress}`
                    });
                    const data = await response.json();
                    if (data.message === "Wallet connected") {
                        window.location.href = '/dashboard';
                    }
                }

                document.getElementById("connectButton").addEventListener("click", connectMetaMask);
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/connect_wallet")
async def connect_wallet(wallet_address: str = Form(...)):
    # Store the wallet address in session or database as needed
    return {"message": "Wallet connected", "wallet_address": wallet_address}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    # Retrieve balance and hashrate from session or database
    balance = 0.0
    hashrate = 1
    html_content = f"""
    <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <h1>Ethereum Mining Dashboard</h1>
            <p>Your Balance: {balance} ETH</p>
            <p>Your Hashrate: {hashrate} GH/s</p>

            <form action="/mine" method="POST">
                <button type="submit">Start Mining</button>
            </form>

            <form action="/upgrade" method="POST">
                <label for="level">Upgrade Miner:</label>
                <select name="level" id="level">
                    <option value="2">Level 2 (2x speed)</option>
                    <option value="3">Level 3 (3x speed)</option>
                    <option value="4">Level 4 (4x speed)</option>
                </select>
                <button type="submit">Upgrade</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/mine")
async def mine():
    # Simulate mining process
    mined_amount = random.uniform(0.0001, 0.001) * 1  # Example calculation
    # Update balance in session or database
    return {"message": f"You mined {mined_amount:.6f} ETH"}

@app.post("/upgrade")
async def upgrade(level: int = Form(...)):
    # Process the upgrade based on the level
    upgrade_cost = {2: 0.01, 3: 0.03, 4: 0.05}.get(int(level), 0)
    return {"message": f"Upgrade to level {level} initiated. Cost: {upgrade_cost} ETH"}
