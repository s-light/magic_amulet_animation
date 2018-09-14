const uint8_t leds_count = 12;
CRGB leds[leds_count];

const uint8_t color_steps = 255 / leds_count;

CRGBPalette16 currentPalette;
TBlendType    currentBlending = LINEARBLEND;

const uint8_t brightness_min = 10;
const uint8_t brightness_max = 255;
uint8_t brightness = 64;

uint16_t update_intervall = 100;



// const TProgmemPalette16 tree_colors_p PROGMEM =
// {
//     // green
//     CHSV( 96, 255, 10),
//     // green
//     CHSV( 96, 255, 255),
//     // yellow
//     CHSV( 64, 255, 255),
//     // blue
//     CHSV( 160, 255, 255),
//     // white
//     CHSV( 160, 0, 255),
// };

// DEFINE_GRADIENT_PALETTE( tree_gp ) {
//       0,    20,100,  0,   //green
//     128,   255,  0,  0,   //yellow
//     224,   255,255,  0,   //blue
//     255,   255,255,255    // white
// };






void ChangePalettePeriodically()
{
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;

    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand == 0)  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 30)  { currentPalette = ForestColors_p;           currentBlending = LINEARBLEND; }
        // if( secondHand == 30)  { currentPalette = tree_gp;           currentBlending = LINEARBLEND; }
    }
}



void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;

    for( int i = 0; i < leds_count; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        // colorIndex += 20;
        colorIndex += color_steps;
    }
}






// ----------------------------------------------------------------------------

void leds_off() {
    FastLED.setBrightness(0);
}







// ----------------------------------------------------------------------------

void fastled_setup(Print &out) {
    // power-up safety delay
    delay(1000);

    // FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, leds_count).setCorrection( TypicalLEDStrip );
    FastLED.addLeds<APA102, RGB>(leds, leds_count);
    FastLED.setBrightness(brightness);

    currentPalette = ForestColors_p;
    currentBlending = LINEARBLEND;
}

void fastled_update() {
    ChangePalettePeriodically();

    static uint8_t startIndex = 0;

    // FastLED based non-blocking delay to update/display the sequence.
    EVERY_N_MILLISECONDS(100) {
        // motion speed
        startIndex = startIndex + 1;
    }

    FillLEDsFromPaletteColors( startIndex);

    FastLED.show();
    FastLED.delay(update_intervall);
}
