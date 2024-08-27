import os
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
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/web3/dist/web3.min.js"></script>
            <script src="https://unpkg.com/@walletconnect/client@1.7.5/dist/umd/index.min.js"></script>
            <script src="https://unpkg.com/@walletconnect/qrcode-modal@1.5.1/dist/umd/index.min.js"></script>
        </head>
        <body>
            <h1>Welcome to Ethereum Mining WebApp</h1>
            <button id="connectButton">Connect MetaMask Wallet</button>

            <script>
                async function connectWallet() {
                    const WalletConnect = window.WalletConnect.default;
                    const connector = new WalletConnect({
                        bridge: "https://bridge.walletconnect.org", // Required
                    });

                    // Check if connection is already established
                    if (!connector.connected) {
                        // Create a new session
                        await connector.createSession();

                        // Get the session URI (deep link)
                        const sessionUri = connector.uri;
                        const deepLink = `https://metamask.app.link/wc?uri=${encodeURIComponent(sessionUri)}`;

                        // Open MetaMask using the deep link
                        window.open(deepLink, "_self");  // "_self" opens in the same tab, necessary on mobile
                    }

                    // Subscribe to connection events
                    connector.on("connect", async (error, payload) => {
                        if (error) {
                            console.error("Connection error", error);
                            return;
                        }

                        // Get provided accounts and chainId
                        const { accounts, chainId } = payload.params[0];
                        console.log("Connected account:", accounts[0]);
                        console.log("Connected chainId:", chainId);

                        // Send the wallet address to the backend
                        const response = await fetch('/connect_wallet', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: `wallet_address=${accounts[0]}`
                        });

                        if (response.ok) {
                            window.location.href = '/dashboard';
                        } else {
                            console.error("Failed to connect wallet on backend");
                        }
                    });

                    // Handle session updates (optional)
                    connector.on("session_update", (error, payload) => {
                        if (error) {
                            console.error("Session update error", error);
                            return;
                        }

                        const { accounts, chainId } = payload.params[0];
                        console.log("Session updated:", accounts, chainId);
                    });

                    // Handle disconnection
                    connector.on("disconnect", (error, payload) => {
                        if (error) {
                            console.error("Disconnect error", error);
                            return;
                        }

                        console.log("Disconnected", payload);
                        // Handle disconnect logic here (optional)
                    });
                }

                document.getElementById("connectButton").addEventListener("click", connectWallet);
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
