---
title: JUCEでバイクアッドフィルターを実装する
title_en: Implementing a Biquad Filter in JUCE
date: 2026-04-01
tags: JUCE, C++, DSP
description: バイクアッドフィルターの理論からJUCEでの実装まで、実際のコードを交えて解説します。
description_en: A walkthrough of biquad filter theory and implementation in JUCE, with real code examples.
---

## はじめに

バイクアッドフィルターはDSPの基礎中の基礎ですが、JUCEで実装するときに少し迷ったのでまとめます。

## 基本的なコード

```cpp
float processSample(float input)
{
    float output = b0 * input + b1 * x1 + b2 * x2
                              - a1 * y1 - a2 * y2;
    x2 = x1; x1 = input;
    y2 = y1; y1 = output;
    return output;
}
```

## 係数の計算

ローパスフィルターの場合、カットオフ周波数 `fc` とサンプルレート `fs` から係数を計算します。

```cpp
void setLowPass(float fc, float fs, float Q)
{
    float w0 = 2.0f * MathConstants<float>::pi * fc / fs;
    float alpha = std::sin(w0) / (2.0f * Q);

    b0 =  (1.0f - std::cos(w0)) / 2.0f;
    b1 =   1.0f - std::cos(w0);
    b2 =  (1.0f - std::cos(w0)) / 2.0f;
    float a0 =  1.0f + alpha;
    a1 = -2.0f * std::cos(w0);
    a2 =  1.0f - alpha;

    // a0で正規化
    b0 /= a0; b1 /= a0; b2 /= a0;
    a1 /= a0; a2 /= a0;
}
```

## まとめ

JUCEには `dsp::IIR::Filter` という組み込みクラスもありますが、自前実装の方が挙動を把握しやすいです。
