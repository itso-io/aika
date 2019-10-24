import React from 'react';
import { withRouter } from "react-router-dom";
import Container from '@material-ui/core/Container';
import {connect} from 'react-redux';


class Footer extends React.Component {
  render() {
    return (
      <div style={{width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', bottom: 0}}>
        <Container maxWidth="md" justify="center" style={{  }}>
          <p>
            We &#10084;&#65039; &#10084;&#65039; &#10084;&#65039; feedback and feature requests. Email us at help@getaika.com, or add requests <a href="https://trello.com/b/KR2vqVGw/aika-product-requests" target="_blank">here</a>.
          </p>
        </Container>
      </div>
    );
  }
}

export default Footer;
