const uint8_t leds_count = 12;
CRGB leds[leds_count];

const uint8_t color_steps = 255 / leds_count;

CRGBPalette16 currentPalette;
CRGBPalette16 targetPalette;
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



// Fill a range of LEDs with a sequece of entryies from a palette in backwards order
// based on https://github.com/FastLED/FastLED/blob/master/colorutils.h#L1554
template <typename PALETTE>
void fill_palette_backwards(
    CRGB* L, uint16_t N, uint8_t startIndex, uint8_t incIndex,
    const PALETTE& pal, uint8_t brightness, TBlendType blendType
) {
    uint8_t colorIndex = startIndex;
    for( uint16_t i = 0; i < N; i++) {
        L[i] = ColorFromPalette( pal, colorIndex, brightness, blendType);
        colorIndex += incIndex;
    }
}


void ChangePalettePeriodically() {
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;

    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand == 0)  {
            targetPalette = CloudColors_p;
        }
        if( secondHand == 30)  {
            targetPalette = ForestColors_p;
        }
    }
}



void FillLEDsFromPaletteColors( uint8_t colorIndex) {
    uint8_t brightness = 255;

    for( int i = 0; i < leds_count; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        // colorIndex += 20;
        colorIndex += color_steps;
    }
}






// ----------------------------------------------------------------------------

void leds_lowbat() {
    // FastLED.setBrightness(1);
}

void handle_lowbat_state() {
    if (!output_enabled) {
        fill_solid(leds, leds_count, CRGB(0, 0, 0));
        EVERY_N_MILLISECONDS(3000) {
            leds[5] = CRGB(255, 0, 0);
            FastLED.delay(50);
            leds[5] = CRGB(0, 0, 0);
        }
    }
}





// ----------------------------------------------------------------------------

void fastled_setup(Print &out) {
    // power-up safety delay
    delay(1000);

    // FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, leds_count).setCorrection( TypicalLEDStrip );
    FastLED.addLeds<APA102, BGR>(leds, leds_count);
    FastLED.setBrightness(brightness);

    currentPalette = ForestColors_p;
    targetPalette = CloudColors_p;
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


    EVERY_N_MILLISECONDS(10) {
        uint8_t maxChanges = 24;
        nblendPaletteTowardPalette( currentPalette, targetPalette, maxChanges);
    }

    FillLEDsFromPaletteColors( startIndex);

    // this overwrittes all other led settings..
    handle_lowbat_state();

    FastLED.show();
    FastLED.delay(update_intervall);
}
