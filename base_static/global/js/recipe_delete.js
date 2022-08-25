function delete_recipe() {
  console.log("opa");
  const forms = document.querySelectorAll(".form-delete");

  for (const form of forms) {
    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        const confirmed = confirm("Are you sure you want to delete");
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
}

delete_recipe();
