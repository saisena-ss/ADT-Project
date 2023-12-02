import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button, IconButton } from '@material-ui/core';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@material-ui/icons';
// Import your Add/Edit modal components here

const Company=()=> {
    const [companies, setCompanies] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [openAddEditModal, setOpenAddEditModal] = useState(false);
    const [editingCompany, setEditingCompany] = useState(null);

    useEffect(() => {
        fetchCompanies();
    }, []);

    const fetchCompanies = () => {
        axios.get('http://127.0.0.1:5000/company') // Adjust API endpoint accordingly
            .then(response => setCompanies(response.data))
            .catch(error => console.error('Error fetching companies', error));
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
        axios.delete(`/api/companies/${companyId}`) // Adjust API endpoint accordingly
            .then(() => fetchCompanies())
            .catch(error => console.error('Error deleting company', error));
    };

    const filteredCompanies = companies.filter(company =>
        company.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <TextField
                label="Search Companies"
                variant="outlined"
                fullWidth
                value={searchTerm}
                onChange={handleSearchChange}
                style={{ marginBottom: 20 }}
            />
            <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleAddCompany}
                style={{ marginBottom: 20 }}
            >
                Add Company
            </Button>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell align="right">Rating</TableCell>
                            {/* Add other headers based on your data */}
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredCompanies.map((company) => (
                            <TableRow key={company.id}>
                                <TableCell>{company.name}</TableCell>
                                <TableCell align="right">{company.rating}</TableCell>
                                {/* Add other cells based on your data */}
                                <TableCell align="right">
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
        </div>
    );
}

export default Company;
