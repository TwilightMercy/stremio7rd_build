const stremioLink = `${window.location.host}/${window.LATEST_VERSION}/manifest.json`;
console.log(stremioLink)

const installAddon = async () => {
    window.location.href = `stremio://${stremioLink}`;
};

const copyConfig = async () => {
    await navigator.clipboard.writeText(`https://${stremioLink}`);
    alert("הקישור הועתק בהצלחה!\nהדבק את הקישור בחיפוש בעמוד ה-Addons.");
};


window.installAddon = installAddon;
window.copyConfig = copyConfig;