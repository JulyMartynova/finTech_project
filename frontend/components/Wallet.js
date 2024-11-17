import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import WalletList from './WalletList';
import CreateWallet from './CreateWallet';

const Wallet = ({ token }) => {
  return (
    <Router>
      <Switch>
        <Route exact path="/wallets" render={() => <WalletList token={token} />} />
        <Route path="/wallets/create" render={() => <CreateWallet token={token} />} />
      </Switch>
    </Router>
  );
};

export default Wallet;