// Function to update and initialize the stremioLink
const updateStremioLink = () => {
    let stremioLink = `${window.location.host}/current_version=${window.LATEST_VERSION},show_catalog_even_if_updated=${window.SHOW_CATALOG_EVEN_IF_UPDATED}/manifest.json`;

    console.log(stremioLink);  // Log the link for debugging
    return stremioLink;  // Return the updated link
};

// Initialize the stremioLink
let stremioLink = updateStremioLink();
console.log(stremioLink)

const installAddon = async () => {
    window.location.href = `stremio://${stremioLink}`;
};

const copyConfig = async () => {
    await navigator.clipboard.writeText(`https://${stremioLink}`);
    alert("הקישור הועתק בהצלחה!\nהדבק את הקישור בחיפוש בעמוד ה-Addons.");
};

// Listen to radio button changes and update SHOW_CATALOG_EVEN_IF_UPDATED
document.getElementById('showCatalogRadio').addEventListener('change', function(event) {
    // Check which radio button is selected
    if (event.target.name === 'showCatalog') {
        window.SHOW_CATALOG_EVEN_IF_UPDATED = event.target.value === 'yes';  // Set to true if 'yes'
        stremioLink = updateStremioLink();  // Update stremioLink when the radio button changes
    }
});


window.installAddon = installAddon;
window.copyConfig = copyConfig;