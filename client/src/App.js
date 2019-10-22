import React from "react";
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Analyses from './components/Analytics/index';
import DatabaseDetails from './components/DatabaseDetails';
import Nav from './components/Nav';
import SignInButton from './components/SignIn';

export default function App() {
  console.log('test');
  return (
    <Router>
      <React.Fragment>
        <CssBaseline />
        <Container>
          <Nav />
          <div style={{width: '100%'}}>
            <Switch>
              <Route path="/database">
                <DatabaseDetails />
              </Route>
              <Route path="/analytics">
                <Analyses />
              </Route>
              <Route path="/">
                <SignInButton />
              </Route>
            </Switch>
          </div>
        </Container>
      </React.Fragment>
    </Router>
  );
}
