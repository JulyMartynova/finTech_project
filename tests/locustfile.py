from locust import HttpUser, task, between

class CryptoExchangeUser(HttpUser):
    wait_time = between(1, 2.5)

    @task 
    def register(self):
        self.client.post("/register", json = {
            "username" : "testuser",
            "password" : "testpassword",
        })
    

    @task 
    def login(self):
        response = self.client.post("/login", json = {
            "username" : "testuser",
            "password" : "testpassword",
        })
        self.token = response.json()["token"]
    

    @task 
    def create_hot_wallet_route(self):
        self.client.post("/wallets/create/hot_wallet", headers={"Authorization:" : f"Bearer {self.token}"})
    

    @task 
    def create_cold_wallet_route(self):
        self.client.post("/wallets/create/cold_wallet", headers={"Authorization" : f"Bearer {self.token}"})
    
    @task
    def create_order_route(self):
        self.client.post("/order", 
                         json = {
                             "wallet_id" : 1,
                             "type" : "buy",
                             "price" : 100,
                             "quantity" : 1
                         },
                         headers={"Authorization", f"Bearer {self.token}"})

    @task 
    def get_wallets_route(self):
        self.client.get("/wallets", headers = {"Authorization:" : f"Bearer {self.token}"})
