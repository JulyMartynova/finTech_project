import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Wallet from './Wallet';
import CreateWallet from './CreateWallet';
import Order from './Order';
import OrderBook from './OrderBook';

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() => <Login setToken={setToken} />} />
        <Route path="/register" component={Register} />
        <Route path="/wallets" render={() => <Wallet token={token} />} />
        <Route path="/wallets/create" render={() => <CreateWallet token={token} />} />
        <Route path="/order" render={() => <Order token={token} />} />
        <Route path="/order-book" render={() => <OrderBook token={token} />} />
      </Switch>
    </Router>
  );
};

export default App;