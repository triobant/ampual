import React, { useState } from 'react';

const PlantForm = ({ handleSearch }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const handleChange = (e) => {
        setSearchTerm(e.target.value);
        handleSearch(e.target.value);
    };

    return (
        <div className="mt-4">
            <input
                type="text"
                placeholder="Search plants..."
                value={searchTerm}
                onChange={handleChange}
                className="border rounded-md px-2 py-1 w-full"
            />
        </div>
    );
};

export default PlantForm;
