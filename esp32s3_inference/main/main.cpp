#include <cstdio>

#include "esp_timer.h"

#include "dl_detect_espdet_postprocessor.hpp"
#include "dl_image_preprocessor.hpp"
#include "dl_model_base.hpp"

// Files embedded into the firmware by main/CMakeLists.txt
extern const uint8_t model_espdl[] asm("_binary_espdet_pico_128_160_espdl_start");
extern const uint8_t image_start[] asm("_binary_test_image_rgb_start");

static constexpr int IMG_W = 160;
static constexpr int IMG_H = 128;
static constexpr int N_RUNS = 20;

static constexpr float CONF_THRESH = 0.5f;
static constexpr float NMS_THRESH = 0.7f;
static constexpr uint32_t MAX_DETECTIONS = 10;

extern "C" void app_main(void)
{
    // Input image: raw RGB888, 160x128
    dl::image::img_t img = {};
    img.data = (void *)image_start;
    img.width = IMG_W;
    img.height = IMG_H;
    img.pix_type = dl::image::DL_IMAGE_PIX_TYPE_RGB888;

    // Load the model and set up pre/post-processing
    dl::Model *model = new dl::Model((const char *)model_espdl, fbs::MODEL_LOCATION_IN_FLASH_RODATA);
    auto *pre = new dl::image::ImagePreprocessor(model, {0, 0, 0}, {255, 255, 255});
    // pre->enable_letterbox({114, 114, 114}); // using rect so no need for letterbox
    auto *post = new dl::detect::ESPDetPostProcessor(
        model, pre, CONF_THRESH, NMS_THRESH, MAX_DETECTIONS, {{8, 8, 4, 4}, {16, 16, 8, 8}, {32, 32, 16, 16}});

    // Run the full pipeline N_RUNS times and time it
    int64_t start = esp_timer_get_time();
    int64_t inference_sum = 0;
    for (int i = 0; i < N_RUNS; i++) {
        pre->preprocess(img);
        int64_t inference_start = esp_timer_get_time();
        model->run();
        inference_sum = esp_timer_get_time() - inference_start;
        post->clear_result();
        post->postprocess();
    }
    int64_t avg_inference_us = inference_sum / N_RUNS;
    int64_t avg_us = (esp_timer_get_time() - start) / N_RUNS;

    printf("Average time per image: %.1f ms\n", avg_us / 1000.0);
    printf("Average inference time: %.1f ms\n", avg_inference_us / 1000.0);

    auto results = post->get_result(img.width, img.height);
    printf("Detections: %u\n", (unsigned)results.size());
    for (const auto &r : results) {
        printf("  ball score %.2f, box (%d, %d) - (%d, %d)\n", r.score, r.box[0], r.box[1], r.box[2], r.box[3]);
    }
}
