/**
 * Formats a pet breed name by replacing underscores with spaces
 * and capitalizing the first letter of each word.
 * @param {string} name - The raw breed name from data or AI result.
 * @returns {string} - The formatted name.
 */
export const formatBreedName = (name) => {
    if (!name) return ''
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase())
}
