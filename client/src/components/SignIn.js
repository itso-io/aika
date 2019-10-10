import React from 'react';
import Container from '@material-ui/core/Container';

const signinUrl = document.location.hostname === 'localhost'
  ? 'http://localhost:5000/auth/google/init' : '/auth/google/init';

const SignInButton = () => (
    <Container maxWidth="sm">
      <div style={{width: '100%', marginTop: '50px',
                   display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <p>
          Welcome to Aika! To get started, sign in with Google and authorize access to your Google Calendar.
        </p>
        <a href={signinUrl}>
          <img src="/google_signin.png" width="250" />
        </a>
      </div>
    </Container>
);

export default SignInButton;
