import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const ProtectedRoute = ({ component: Component, token, ...rest }) => {
  return (
    <Route
      {...rest}
      render={(props) =>
        token ? <Component {...props} token={token} /> : <Redirect to="/" />
      }
    />
  );
};

export default ProtectedRoute;