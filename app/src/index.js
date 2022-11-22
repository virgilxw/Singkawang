import React from 'react';
import {Helmet} from "react-helmet";
import ReactDOM from 'react-dom/client';
import App from './App';
import CssBaseline from '@mui/material/CssBaseline';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <Helmet>
      <title>The Temples of Singkawang</title>
    <meta name="viewport" content="initial-scale=1, width=device-width" />
    </Helmet>
    <CssBaseline />
    <App />
  </>
);