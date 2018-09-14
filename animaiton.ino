const uint8_t leds_count = 12;
CRGB leds[leds_count];

const uint8_t color_steps = 255 / (leds_count/2);

CRGBPalette16 currentPalette;
CRGBPalette16 targetPalette;
TBlendType    currentBlending = LINEARBLEND;

const uint8_t brightness_min = 10;
const uint8_t brightness_max = 255;
uint8_t brightness = 10;

uint16_t update_intervall = 10;

uint16_t fade_intervall = 10;

bool leds_highlight = false;

// DEFINE_GRADIENT_PALETTE( tree_gp ) {
//       0,    20,100,  0,   //green
//     128,   255,  0,  0,   //yellow
//     224,   255,255,  0,   //blue
//     255,   255,255,255    // white
// };
// DEFINE_GRADIENT_PALETTE( tree_gp ) {
//       0,    20,100,  0,   //green
//     128,   255,  0,  0,   //yellow
//     224,   255,255,  0,   //blue
//     255,   CHSV( 150, 200, 100)    // white
// };

//
CRGBPalette16 tree_palette1(
    // white
    CHSV( 150, 200, 100),
    // blue
    CHSV( 150, 255, 150),
    // // green
    // CHSV( 90, 255, 255),
    // green
    CHSV( 80, 255, 150),
    // yellow
    CHSV( 64, 255, 255)
);

CRGBPalette16 tree_palette2(
    // white
    CHSV( 150, 200, 100),
    // blue
    CHSV( 150, 255, 150),
    // blue
    CHSV( 150, 255, 150),
    // green
    CHSV( 90, 255, 255),

    // white
    CHSV( 150, 200, 100),
    // blue
    CHSV( 150, 255, 150),
    // blue
    CHSV( 150, 255, 150),
    // green
    CHSV( 90, 255, 255),

    // green
    CHSV( 80, 255, 150),
    // yellow
    CHSV( 64, 255, 255),
    // green
    CHSV( 80, 255, 150),
    // yellow
    CHSV( 64, 255, 255),

    // green
    CHSV( 80, 255, 150),
    // yellow
    CHSV( 64, 255, 255),
    // green
    CHSV( 80, 255, 150),
    // yellow
    CHSV( 64, 255, 255)
);

CRGBPalette16 tree_highlight(
    // purple
    CHSV( 192, 255, 100),
    // blue
    CHSV( 160, 255, 255),
    // dark blue
    CHSV( 170, 255, 150)
);


void ChangePalettePeriodically() {
    uint8_t secondHand = (millis() / 1000) % 40;
    static uint8_t lastSecond = 99;

    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand == 0)  {
            targetPalette = tree_palette1;
            Serial.println(F("tree_palette1"));
        }
        if( secondHand == 20)  {
            targetPalette = tree_palette2;
            Serial.println(F("tree_palette2"));
        }
    }
}



void FillLEDsFromPaletteColorsSymetrical( uint8_t colorIndex) {
    uint8_t brightness = 255;
    for( int i = 0; i < (leds_count/2); i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        leds[leds_count-i-1] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
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


void highlight_on() {
    leds_highlight = true;
    fade_intervall = 10;
    // FastLED.setBrightness(255);
    targetPalette =  tree_highlight;
}

void highlight_off() {
    leds_highlight = false;
    fade_intervall = 1000;
    // FastLED.setBrightness(brightness);
    targetPalette = tree_palette1;
}


// ----------------------------------------------------------------------------

void fastled_setup(Print &out) {
    // power-up safety delay
    delay(1000);

    // FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, leds_count).setCorrection( TypicalLEDStrip );
    FastLED.addLeds<APA102, BGR>(leds, leds_count);
    FastLED.setBrightness(brightness);

    currentBlending = LINEARBLEND;
    // currentPalette = ForestColors_p;
    // targetPalette = CloudColors_p;
    currentPalette = tree_palette1;
    targetPalette =  tree_palette1;
}

void fastled_update() {

    if (!leds_highlight) {
        ChangePalettePeriodically();
    }

    static uint8_t startIndex = 0;

    // // FastLED based non-blocking delay to update/display the sequence.
    // EVERY_N_MILLISECONDS(100) {
    //     // motion speed
    //     startIndex = startIndex + 1;
    // }

    if (leds_highlight) {
        EVERY_N_MILLISECONDS(10) {
            uint8_t maxChanges = 24;
            nblendPaletteTowardPalette( currentPalette, targetPalette, maxChanges);
        }
    } else {
        EVERY_N_MILLISECONDS(100) {
            uint8_t maxChanges = 24;
            nblendPaletteTowardPalette( currentPalette, targetPalette, maxChanges);
        }
    }

    // FillLEDsFromPaletteColors(startIndex);
    FillLEDsFromPaletteColorsSymetrical(startIndex);

    // this overwrittes all other led settings..
    handle_lowbat_state();

    FastLED.show();
    // FastLED.delay(update_intervall);
}
