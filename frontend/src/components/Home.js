import React, { useState, useEffect } from 'react';
import PlantForm from './PlantForm';
import PlantList from './PlantList';

const Home = () => {
    const [plants, setPlants] = useState([]);
    const [filteredPlants, setFilteredPlants] = useState([]);

    useEffect(() => {
        fetchPlants();
    }, []);

    const fetchPlants = async () => {
        try {
            const response = await fetch('/api/plants');
            const data = await response.json();
            setPlants(data);
            setFilteredPlants(data);
        } catch (error) {
            console.error('Error fetching plants:', error);
        }
    };

    const handleSearch =  async (query) => {
        try {
            const response = await fetch('/api/plants/?query=${query}');
            const data = await response.json();
            setFilteredPlants(data);
        } catch (error) {
            console.error('Error searching plants:', error)
        }
    };

    return (
        <div>
            <h1 className="text-2xl font-semibold mb-4">Ampual - PLACEHOLDER TEXT</h1>
            <PlantForm handleSearch={handleSearch} />
            <PlantList plants={filteredPlants} />
        </div>
    );
};

export default Home;
