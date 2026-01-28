import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Project root
const projectRoot = path.resolve(__dirname, '../../../');

// Paths
const inputFile = path.join(projectRoot, 'ai', 'data', 'metadata.csv');
const outputFile = path.join(projectRoot, 'frontend', 'src', 'data', 'pets_data.json');

// Ensure output directory exists
fs.mkdirSync(path.dirname(outputFile), { recursive: true });

/* ================= CSV PARSER ================= */

const parseCSV = (text) => {
    const rows = [];
    let row = [];
    let cell = '';
    let inQuote = false;

    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        const n = text[i + 1];

        if (c === '"') {
            if (inQuote && n === '"') {
                cell += '"';
                i++;
            } else {
                inQuote = !inQuote;
            }
        } else if (c === ',' && !inQuote) {
            row.push(cell);
            cell = '';
        } else if ((c === '\n' || c === '\r') && !inQuote) {
            if (c === '\r' && n === '\n') i++;
            row.push(cell);
            rows.push(row);
            row = [];
            cell = '';
        } else {
            cell += c;
        }
    }
    return rows;
};

/* ================= MAIN ================= */

fs.readFile(inputFile, 'utf8', (err, text) => {
    if (err) {
        console.error('❌ Read CSV error:', err);
        return;
    }

    const rows = parseCSV(text);
    const dataRows = rows.slice(1); // skip header

    const pets = dataRows.map(row => {
        const get = i => (row[i] || '').trim();
        const rawName = get(2);
        const name = rawName.replace(/_/g, ' ').trim();
        if (!name) return null;

        const slug = name.toLowerCase().replace(/\s+/g, '_');

        // Prices
        const pricePaper = get(8);
        const priceNoPaper = get(9);
        const priceInternational = get(10);

        // Parse numeric prices
        const allPrices = `${pricePaper} ${priceNoPaper} ${priceInternational}`;
        const nums = allPrices.match(/\d+/g)?.map(Number) || [];
        const priceMin = nums.length ? Math.min(...nums) : 0;
        const priceMax = nums.length ? Math.max(...nums) : 0;

        // Scores
        const scoreEnergy = parseInt(get(11)) || 3;
        const scoreSpace = parseInt(get(12)) || 3;
        const scoreGrooming = parseInt(get(13)) || 3;
        const scoreKid = parseInt(get(14)) || 3;

        // Size from score_size
        const rawSize = get(15); // small | medium | large
        let size = 'Trung bình';
        if (rawSize === 'small') size = 'Nhỏ';
        if (rawSize === 'large') size = 'Lớn';

        return {
            id: slug,
            name: name,
            type: get(1),
            lifespan: get(3),
            care_instruction: get(7),
            price: {
                paper: pricePaper,
                no_paper: priceNoPaper,
                international: priceInternational
            },
            priceMin,
            priceMax,
            size,
            scores: {
                energy: scoreEnergy,
                space: scoreSpace,
                grooming: scoreGrooming,
                kid_friendly: scoreKid
            },
            image_path: `/assets/avatar/${slug}.jpg`
        };
    }).filter(Boolean);

    fs.writeFile(
        outputFile,
        JSON.stringify(pets, null, 2),
        'utf8',
        err => {
            if (err) console.error('❌ Write JSON error:', err);
            else console.log(`✅ Converted ${pets.length} pets → pets_data.json`);
        }
    );
});
