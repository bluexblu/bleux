from django import forms
from inventario.models import Usuario  # Asegúrate de que el modelo Usuario esté correctamente importado

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class RegistroForm(forms.ModelForm):
    # Campos adicionales si es necesario (por ejemplo, confirmación de contraseña)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = Usuario  # Usa el modelo de Usuario definido en tu proyecto
        fields = ['email', 'password', 'nombre', 'codigo_verificacion']  # Ajusta los campos según tu modelo

    def clean_email(self):
        """Verifica si el correo ya está registrado"""
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_password(self):
        """Verifica que la contraseña tenga al menos 8 caracteres"""
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password

    def clean_password_confirmation(self):
        """Verifica que la contraseña y la confirmación sean iguales"""
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password_confirmation
