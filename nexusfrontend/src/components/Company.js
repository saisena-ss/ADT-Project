import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button, IconButton, Typography, Container } from '@material-ui/core';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@material-ui/icons';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(3),
  },
  title: {
    flex: '1 1 100%',
    margin: theme.spacing(2, 0),
  },
  addButton: {
    float: 'right',
    marginBottom: theme.spacing(2),
  },
  searchField: {
    marginBottom: theme.spacing(2),
    marginRight: theme.spacing(2),
  },
  table: {
    minWidth: 650,
  },
  tableHeader: {
    fontWeight: 'bold', // Make table headers bold
  },
  actionCell: {
    width: '130px',
    fontWeight: 'bold'
  },
}));

const baseUrl = "http://127.0.0.1:5000";

const Company = () => {
  const classes = useStyles();
  
  const [companies, setCompanies] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [openAddEditModal, setOpenAddEditModal] = useState(false);
    const [editingCompany, setEditingCompany] = useState(null);

    useEffect(() => {
        fetchCompanies();
        console.log(companies);
    }, []);

    const fetchCompanies = async() => {
        try{
            const response = await fetch(baseUrl + '/company');
            const dataArray = await response.json();
            const transformedData = dataArray.map(item => ({
                id: item[0],
                name: item[1].split('\n')[0], // Assuming name and rating are in the format "Name\nRating"
                rating: item[1].split('\n')[1],
                founded: item[2],
                // Add other properties based on their position in the array
                headquarters: item[3],
                size: item[4],
                revenue: item[5],
                type: item[6],
                industry: item[7],
                sector: item[8]
            }));
            console.log(transformedData);
            setCompanies(transformedData);
        } catch (error){
            console.error('Something wrong happened!')
        }
    };

    const handleSearchChange = event => {
        setSearchTerm(event.target.value);
    };

    const handleAddCompany = () => {
        setEditingCompany(null);
        setOpenAddEditModal(true);
    };

    const handleEditCompany = company => {
        setEditingCompany(company);
        setOpenAddEditModal(true);
    };

    const handleDeleteCompany = companyId => {
       const r = 2;   };

    const filteredCompanies = companies.filter(company =>
        company.name.toLowerCase().includes(searchTerm.toLowerCase())
    );


  return (
    <Container className={classes.container} maxWidth="xl">
      <Typography className={classes.title} variant="h4" component="h1" gutterBottom>
        Company Dashboard
      </Typography>
      <div>
        <TextField
          className={classes.searchField}
          label="Search Companies"
          variant="outlined"
          value={searchTerm}
          onChange={handleSearchChange}
        />
        <Button width='lg'
          className={classes.addButton}
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleAddCompany}
        >
          Add Company
        </Button>
      </div>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead className={classes.tableHeader}>
            <TableRow>
              <TableCell className={classes.tableHeader}>Name</TableCell>
              <TableCell className={classes.tableHeader} align="right">Rating</TableCell>
              <TableCell className={classes.tableHeader} align="right">Founded</TableCell>
              <TableCell className={classes.tableHeader} align="right">Headquarters</TableCell>
              <TableCell className={classes.tableHeader} align="right">Size</TableCell>
              <TableCell className={classes.tableHeader} align="right">Revenue</TableCell>
              <TableCell className={classes.tableHeader} align="right">Type</TableCell>
              <TableCell className={classes.tableHeader} align="right">Industry</TableCell>
              <TableCell className={classes.tableHeader} align="right">Sector</TableCell>
              <TableCell className={classes.actionCell} align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredCompanies.map((company) => (
              <TableRow key={company.id}>
                <TableCell component="th" scope="row">{company.name}</TableCell>
                <TableCell align="right">{company.rating}</TableCell>
                <TableCell align="right">{company.founded}</TableCell>
                <TableCell align="right">{company.headquarters}</TableCell>
                <TableCell align="right">{company.size}</TableCell>
                <TableCell align="right">{company.revenue}</TableCell>
                <TableCell align="right">{company.type}</TableCell>
                <TableCell align="right">{company.industry}</TableCell>
                <TableCell align="right">{company.sector}</TableCell>
                <TableCell className={classes.actionCell} align="right">
                  <IconButton onClick={() => handleEditCompany(company)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDeleteCompany(company.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {/* Add/Edit Modal - Implement this component based on your requirement */}
      {/* <AddEditCompanyModal open={openAddEditModal} onClose={() => setOpenAddEditModal(false)} company={editingCompany} onSave={fetchCompanies} /> */}
    </Container>
  );
};

export default Company;
