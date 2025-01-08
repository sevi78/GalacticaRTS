
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Normalize coordinates
    vec2 uv = fragCoord / iResolution.xy;
    vec2 center = vec2(0.5, 0.5);
    vec2 mousePos = iMouse.xy / iResolution.xy;

    // Calculate direction from center to mouse
    vec2 direction = mousePos - center;
    float lineLength = length(direction);

    // Calculate distance from current pixel to the line segment
    vec2 lineDir = normalize(direction);
    vec2 perpDir = vec2(-lineDir.y, lineDir.x);
    float distToLine = abs(dot(uv - center, perpDir));
    float distAlongLine = dot(uv - center, lineDir);

    // Set line thickness
    float thickness = 0.002;

    // Draw the line
    float line = smoothstep(thickness, 0.0, distToLine) *
                 step(0.0, distAlongLine) *
                 step(distAlongLine, lineLength);

    // Output color
    fragColor = vec4(vec3(line), 1.0);
}
