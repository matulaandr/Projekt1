CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
    datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
);
