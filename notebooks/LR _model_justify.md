## ✅ Final Model Choice: Logistic Regression (TF-IDF + L2)

### 1️⃣ Sparse & High-Dimensional Feature Suitability

**Keyword:** **Linear Separability in Text Space**

TF-IDF creates thousands of sparse features where:

* Each word contributes **linearly** to sentiment
* Signal is distributed across many weak predictors

 **Logistic Regression excels in this setup** , whereas XGBoost:

* Is optimized for **dense, interaction-heavy features**
* Struggles to efficiently exploit sparse linear signals

> ✔ Logistic Regression directly models word-weight contributions
>
> ❌ XGBoost attempts unnecessary tree splits on sparse features

---

### 2️⃣ Bias–Variance Balance & Overfitting Control

**Keyword:** **Regularization-Driven Generalization**

* Logistic Regression uses **explicit L2 regularization**
* Regularization strength (`C`) was tuned via **GridSearchCV**
* Delivered **stable cross-validated F1 and accuracy**

XGBoost:

* Has many implicit regularizers
* Requires deeper tuning (`max_depth`, `gamma`, `subsample`)
* Showed **higher variance risk** for this dataset size

> Decision favored **predictable generalization over model complexity**

---

### 3️⃣ Interpretability & Explainability

**Keyword:** **Model Transparency**

Logistic Regression provides:

* Direct access to **feature coefficients**
* Clear explanation of **which words drive sentiment**
* Easier debugging and stakeholder communication

XGBoost:

* Produces **opaque tree ensembles**
* Requires SHAP for interpretability
* Adds operational complexity without performance gain

---

### 4️⃣ Training Efficiency & Experiment Velocity

**Keyword:** **Cost-Effective Experimentation**

| Aspect               | Logistic Regression | XGBoost |
| -------------------- | ------------------- | ------- |
| Training time        | Fast                | Slower  |
| Hyperparameter space | Small               | Large   |
| MLflow tracking      | Clean               | Noisy   |
| Deployment size      | Lightweight         | Heavy   |

> Logistic Regression enabled  **rapid experimentation and reproducibility** , aligning with MLOps best practices.

---

### 5️⃣ Empirical Evidence (MLflow-Driven Decision)

**Keyword:** **Evidence-Based Model Selection**

* MLflow experiments showed **no statistically meaningful performance uplift** from XGBoost
* Logistic Regression achieved:
  * Comparable or better **accuracy & F1**
  * Lower variance across folds
  * Cleaner hyperparameter sensitivity patterns

> Final decision was  **data-driven** , not assumption-driven.

---

## 🏁 Conclusion

> Logistic Regression was selected as the final model due to its superior alignment with sparse TF-IDF features, strong regularization control, interpretability, faster training, and equivalent performance to more complex ensemble methods—making it the most production-ready choice for this problem.
>
