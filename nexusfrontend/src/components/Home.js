// Import React and Material-UI components
import React from 'react';
import { Typography, Container, Grid, Paper, Link } from '@material-ui/core';

const Home=() => {
    return (
        <Container maxWidth="lg" style={{ marginTop: 30 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Job Nexus Dashboard
            </Typography>

            <Grid container spacing={3}>
                {/* Quick Links or Summary Cards */}
                <Grid item xs={12} md={6} lg={4}>
                    <Paper style={{ padding: 20 }}>
                        <Typography variant="h6" gutterBottom>
                            Companies
                        </Typography>
                        <Typography variant="body1">
                            View and manage companies.
                        </Typography>
                        <Link href="/companies">Go to Companies</Link>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6} lg={4}>
                    <Paper style={{ padding: 20 }}>
                        <Typography variant="h6" gutterBottom>
                            Job Postings
                        </Typography>
                        <Typography variant="body1">
                            Explore and post jobs.
                        </Typography>
                        <Link href="/jobpostings">Go to Job Postings</Link>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6} lg={4}>
                    <Paper style={{ padding: 20 }}>
                        <Typography variant="h6" gutterBottom>
                            Job Salaries
                        </Typography>
                        <Typography variant="body1">
                            Explore and post salaries and reviews.
                        </Typography>
                        <Link href="/jobs">Go to Jobs</Link>
                    </Paper>
                </Grid>

                {/* Add more sections as needed */}

                {/* Data Visualization Section */}
                <Grid item xs={12}>
                    <Paper style={{ padding: 20 }}>
                        <Typography variant="h6" gutterBottom>
                            Data Insights
                        </Typography>
                        {/* Data Visualization Components */}
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
}

export default Home;
