import React from 'react';
import Container from '@material-ui/core/Container';

const signinUrl = document.location.hostname === 'localhost'
  ? 'http://localhost:5000/auth/google/init' : '/auth/google/init';

const SignInButton = () => (
    <Container maxWidth="md">
      <div style={{width: '100%', marginTop: '50px',
                   display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <p>
          Welcome to Aika! Aika lets you explore your meetings in Google Calendar with pre-built analytics and
          open-ended SQL access, which you can use with your favorite MySQL client, Looker, Mode,
          or anything else that can make use of a MySQL database.
        </p>
        <p>
          To get started, sign in with Google. Aika requests two permissions:
          <ol>
            <li>
              Read-only access to Google Calendar, so Aika can sync your events and
              event attendees (a.k.a. guests) to the private MySQL database we create for you
            </li>
            <li>
              Read-only access to your G Suite company directory, <i>solely</i> so Aika can
              provide you with a complete list of calendars that you have the option to sync
            </li>
          </ol>
        </p>
        <a href={signinUrl}>
          <img alt="Google signin" src="/images/google_signin.png" width="250" />
        </a>
        <p>
          By signing into Aika, you agree to
          Aika's <a href="https://app.getaika.com/terms">License Agreement</a> and <a href="https://app.getaika.com/privacy">Privacy Policy</a>.
        </p>
      </div>
    </Container>
);

export default SignInButton;
