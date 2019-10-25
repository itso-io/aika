import React from 'react';
import Container from '@material-ui/core/Container';


class Footer extends React.Component {
  render() {
    return (
      <div style={{width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', bottom: 0}}>
        <Container maxWidth="md" justify="center" style={{  }}>
          <p>
            We <span role="img" aria-label="love love LOVE">&#10084;&#65039; &#10084;&#65039; &#10084;&#65039;</span> feedback and feature requests. Email us at <a href="mailto:help@getaika.com">help@getaika.com</a>, or add requests <a href="https://trello.com/b/KR2vqVGw/aika-product-requests" target="_blank" rel="noopener noreferrer">here</a>.
          </p>
        </Container>
      </div>
    );
  }
}

export default Footer;
