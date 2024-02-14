import React from 'react';

const PlantList = ({ plants }) => {
    return (
        <div className="mt-4">
            <h2 className="text-lg font-semibold">Plants</h2>
            <ul className="mt-2">
                {plants.map((plant) => (
                    <li key={plant.id} className="py-1">{plant.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default PlantList;
