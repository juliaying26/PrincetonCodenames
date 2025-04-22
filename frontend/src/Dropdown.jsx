import React, { useState } from 'react';
import Select from 'react-dropdown-select';

export default function Dropdown({ options, selected, setSelected }) {
  const dropdownOptions = options.map((option) => ({
    label: option,
    value: option,
  }));

  return (
    <div className="relative w-64 bg-white rounded-xl">
      <Select
        style={{ fontSize: '1.25rem', padding: '12px', borderRadius: '10px' }}
        options={dropdownOptions}
        values={selected}
        onChange={setSelected}
        placeholder="Guess a word"
        clearable
        dropdownGap={0}
      />
    </div>
  );
}
