/**
 * @author jonobr1 / http://jonobr1.com/
 */

/**
 * Convert r, g, b to normalized vec3
 */
vec3 rgb(float r, float g, float b) {
    return vec3(r / 255.0, g / 255.0, b / 255.0);
}

/**
 * Draw a glowing circle at vec2 `pos` with radius `rad` and
 * color `color`.
 */
vec4 glowingCircle(vec2 uv, vec2 pos, float rad, vec3 color) {
    // Adjust uv for aspect ratio
    float aspectRatio = iResolution.x / iResolution.y;
    uv.x *= aspectRatio; // Scale x coordinate based on aspect ratio

    float d = length(pos - uv); // Distance from the center
    float glowRadius = rad + 0.1; // Radius for the glow effect
    float edgeSoftness = 0.05; // Softness of the glow edge

    // Calculate alpha based on distance from the center
    float alpha = smoothstep(rad, rad + edgeSoftness, d) - smoothstep(glowRadius, glowRadius + edgeSoftness, d);

    // Return color with alpha for glowing effect
    return vec4(color, alpha);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy; // Normalized coordinates (0 to 1)
    vec2 center = vec2(0.5); // Center of the screen in normalized coordinates
    float radius = 0.25; // Radius as a fraction of screen size

    // Background layer
    vec4 layer1 = vec4(rgb(0.0, 0.0, 0.0), 1.0); // Black background

    // Glowing Circle
    vec3 red = rgb(225.0, 95.0, 60.0);
    vec4 layer2 = glowingCircle(uv, center, radius, red);

    // Blend the two layers
    fragColor = mix(layer1, layer2, layer2.a);
}
