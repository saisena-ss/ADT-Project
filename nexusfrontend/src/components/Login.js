// Import React and Material-UI components
import React, { useState } from 'react';
import { TextField, Button, Typography, Container, Paper, Grid } from '@material-ui/core';

const Login=() => {
  // State for form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle login logic here
    console.log(email, password);
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper style={{ padding: 20, marginTop: 50 }}>
        <Typography variant="h5">Login</Typography>
        <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Email Address"
                variant="outlined"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Password"
                type="password"
                variant="outlined"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
              >
                Login
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
}

export default Login;
