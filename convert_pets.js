import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const inputFile = path.join(__dirname, 'dog.csv');
const outputFile = path.join(__dirname, 'src', 'data', 'pets_data.json');

// Ensure output directory exists
const outputDir = path.dirname(outputFile);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

fs.readFile(inputFile, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }

    // Reuse the same parsing logic
    const parseCSV = (text) => {
        const result = [];
        let row = [];
        let inQuote = false;
        let currentCell = '';

        for (let i = 0; i < text.length; i++) {
            const char = text[i];
            const nextChar = text[i + 1];

            if (char === '"') {
                if (inQuote && nextChar === '"') {
                    currentCell += '"';
                    i++; // skip next quote
                } else {
                    inQuote = !inQuote;
                }
            } else if (char === ',' && !inQuote) {
                row.push(currentCell);
                currentCell = '';
            } else if ((char === '\r' || char === '\n') && !inQuote) {
                if (char === '\r' && nextChar === '\n') i++;
                row.push(currentCell);
                if (row.length > 1 || row[0] !== '') { // Skip empty rows
                    result.push(row);
                }
                row = [];
                currentCell = '';
            } else {
                currentCell += char;
            }
        }
        if (row.length > 0) result.push(row);
        return result;
    };

    const rows = parseCSV(data);

    // Config based on the provided CSV structure
    // Row 0: STT, tên giống loài, tuổi thọ trung bình, cách chăm, giá cả trung bình, , , score_energy, score_space, score_grooming, score_kid_friendly, is_cat
    // Row 1: , , , , có giấy tờ, không giấy tờ, quốc tế, , , , ,

    const dataRows = rows.slice(2); // Skip first 2 header rows

    const pets = dataRows.map(row => {
        // Safe access
        const get = (idx) => (row[idx] || '').trim();

        const name = get(1);
        if (!name) return null; // Skip empty rows

        const slug = name.toLowerCase().trim().replace(/\s+/g, '_');
        const lifespan = get(2);
        const care = get(3);

        // Prices
        const pricePaper = get(4);
        const priceNoPaper = get(5);
        const priceInternational = get(6);

        // Scores
        const scoreEnergy = parseInt(get(7)) || 2;
        const scoreSpace = parseInt(get(8)) || 2;
        const scoreGrooming = parseInt(get(9)) || 2;
        const scoreKid = parseInt(get(10)) || 1;
        const isCat = parseInt(get(11)) === 1;

        // Determine Size Category based on Space Score
        let size = 'Trung bình';
        if (scoreSpace === 1) size = 'Nhỏ';
        if (scoreSpace === 3) size = 'Lớn';

        // Extract numeric price for filtering (Approximation)
        const parsePrice = (str) => {
            const numbers = str.match(/(\d+)/g);
            if (!numbers) return 0;
            return parseInt(numbers[0]);
        };

        const priceMin = parsePrice(pricePaper);

        const allPrices = [pricePaper, priceNoPaper, priceInternational].join(' ');
        const priceMatches = allPrices.match(/(\d+)/g);
        let realMin = 0, realMax = 100;
        if (priceMatches) {
            const nums = priceMatches.map(n => parseInt(n));
            realMin = Math.min(...nums);
            realMax = Math.max(...nums);
        }

        return {
            id: slug,
            name: name.replace(/_/g, ' '),
            type: isCat ? 'Cat' : 'Dog',
            lifespan: lifespan,
            care_instruction: care,
            price: {
                paper: pricePaper,
                no_paper: priceNoPaper,
                international: priceInternational
            },
            priceMin: realMin,
            priceMax: realMax,
            size: size,
            scores: {
                energy: scoreEnergy,
                space: scoreSpace,
                grooming: scoreGrooming,
                kid_friendly: scoreKid
            },
            image_path: `/assets/dog_images/${slug}/avatar.jpg`
        };
    }).filter(p => p !== null);

    const jsonContent = JSON.stringify(pets, null, 2);

    fs.writeFile(outputFile, jsonContent, 'utf8', (err) => {
        if (err) {
            console.error('Error writing JSON:', err);
        } else {
            console.log(`Successfully converted ${pets.length} pets to ${outputFile}`);
        }
    });
});
