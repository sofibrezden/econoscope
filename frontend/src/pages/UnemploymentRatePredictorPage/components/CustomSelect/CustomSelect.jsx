import React, { useState, useRef, useEffect } from "react";
import styles from "./CustomSelect.module.scss";

const CustomSelect = ({ options, placeholder, value, onChange }) => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    const handleOptionClick = (option) => {
        onChange(option);
        setIsOpen(false);
    };

    const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setIsOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <div className={styles.customSelect} ref={dropdownRef}>
            <div
                className={`${styles.selectHeader} ${
                    !value ? styles.placeholderActive : ""
                }`}
                onClick={() => setIsOpen(!isOpen)}
            >
                {value ? value.label : <span className={styles.placeholder}>{placeholder}</span>}
                <span className={styles.arrow}>{isOpen ? "▲" : "▼"}</span>
            </div>
            {isOpen && (
                <ul className={styles.optionsList}>
                    {options.map((option) => (
                        <li
                            key={option.value}
                            className={styles.option}
                            onClick={() => handleOptionClick(option)}
                        >
                            {option.label}
                            {(option.value === 2026 || option.value === 2027) && (
                                <span className={styles.lessAccurate}> **Less Accurate</span>
                            )}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomSelect;
