export const getRawControl = (record, targetTime) => {
    const layerControls = record.map(layer => {
        if (layer.v === false) return {};
        const layerData = layer.a;
        const rawControlIndex = layerData?.reduce?.((p, c, i) => c.t <= targetTime ? i : p, undefined);
        if (rawControlIndex === undefined) return {};
        const rawControl = {...layerData[rawControlIndex]?.c};
        const rawControlNext = layerData[rawControlIndex + 1]?.c;
        // console.log(rawControl);
        if (rawControlNext && rawControl.mouseX !== undefined && rawControlNext.mouseX !== undefined) {
            // console.log(rawControl,rawControlNext);
            const lt = layerData[rawControlIndex]?.t;
            const rt = layerData[rawControlIndex + 1]?.t;
            const kl = (rt - targetTime) / (rt - lt);
            const kr = (targetTime - lt) / (rt - lt);
            rawControl.mouseX = rawControl?.mouseX * kl + rawControlNext?.mouseX * kr;
            rawControl.mouseY = rawControl?.mouseY * kl + rawControlNext?.mouseY * kr;
        }
        if (rawControl?.mouseX === undefined) {
            delete rawControl.mouseX;
            delete rawControl.mouseY;
        }
        return rawControl;
    })
    // debugger;
    const newControl = layerControls.reduce((p, c) => ({
        ...p, ...c,
        keyInput: [...(p.keyInput || []), ...(c.keyInput || [])]
    }), {})
    if (newControl?.mouseX === undefined) {
        delete newControl.mouseX;
        delete newControl.mouseY;
    }
    return newControl;
};
