%ifnarch s390x
%global with_hardware 0
%global with_vulkan_hw 0
%global with_vdpau 0
%global with_va 1
%if !0%{?rhel}
%global with_nine 1
%global with_omx 1
%global with_opencl 0
%endif
%global base_vulkan ,amd
%endif

%global qvplibdir /usr/qvp/lib64
%global qvpincludedir /usr/qvp/include
%global qvpdatadir /usr/qvp/share
%global with_opencl 0
%global with_clc 0
%global with_glvnd 0
%ifarch %{ix86} x86_64
%global with_crocus 1
%global with_i915   1
%if !0%{?rhel}
%global with_intel_clc 0
%endif
%global with_iris   1
%global intel_platform_vulkan ,intel,intel_hasvk
%endif

%ifarch aarch64 x86_64 %{ix86}
%if !0%{?rhel}
%global with_lima      1
%global with_vc4       1
%endif
%global with_etnaviv   1
%global with_freedreno 1
%global with_kmsro     1
%global with_panfrost  1
%global with_tegra     1
%global with_v3d       1
%global extra_platform_vulkan ,broadcom,freedreno,panfrost
%endif

%ifnarch s390x
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%endif
%global with_radeonsi 1
%global with_vmware 1
%endif

%if !0%{?rhel}
%global with_libunwind 1
%global with_lmsensors 1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global vulkan_drivers swrast%{?base_vulkan}%{?intel_platform_vulkan}%{?extra_platform_vulkan}

Name:           mesa-qvp
Summary:        Mesa graphics libraries
%global 	ver 23.2.0
Version:        23.2.0
Release:       	r0
License:        MIT AND BSD-3-Clause AND SGI-B-2.0
URL:            http://www.mesa3d.org

Source0:        mesa-qvp-23.2.0.tar.gz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
%if 0%{?with_hardware}
BuildRequires:  kernel-headers
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm)
%if 0%{?with_libunwind}
BuildRequires:  pkgconfig(libunwind)
%endif
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.8
BuildRequires:  pkgconfig(wayland-client) >= 1.11
BuildRequires:  pkgconfig(wayland-server) >= 1.11
BuildRequires:  pkgconfig(wayland-egl-backend) >= 3
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xdamage) >= 1.1
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2) >= 1.8
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xshmfence) >= 1.1
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(glproto) >= 1.4.14
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xrandr) >= 1.3
BuildRequires:  bison
BuildRequires:  flex
%if 0%{?with_lmsensors}
BuildRequires:  lm_sensors-devel
%endif
%if 0%{?with_vdpau}
BuildRequires:  pkgconfig(vdpau) >= 1.1
%endif
%if 0%{?with_va}
BuildRequires:  pkgconfig(libva) >= 0.38.0
%endif
%if 0%{?with_omx}
BuildRequires:  pkgconfig(libomxil-bellagio)
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  llvm-devel >= 7.0.0
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif

%description
Mesa Drivers.

%package libGL
Summary:        Mesa libGL runtime libraries

%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Provides:       libGL-devel
Provides:       libGL-devel%{?_isa}

%description libGL-devel
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-qvp-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description filesystem
%{Summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries

%description libEGL
%{Summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Provides:       libEGL-devel
Provides:       libEGL-devel%{?_isa}

%description libEGL-devel
%{Summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers

%description dri-drivers
%{Summary}.

%package libOSMesa
Summary:        Mesa offscreen rendering libraries
Provides:       libOSMesa
Provides:       libOSMesa-%{?_isa}

%description libOSMesa
%{Summary}.

%package libOSMesa-devel
Summary:        Mesa offscreen rendering development package

%description libOSMesa-devel
%{Summary}.

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm
Provides:       libgbm%{?_isa}
# If mesa-dri-drivers are installed, they must match in version. This is here to prevent using
# older mesa-dri-drivers together with a newer mesa-libgbm and its dependants.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2193135 .

%description libgbm
%{Summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Provides:       libgbm-devel
Provides:       libgbm-devel%{?_isa}

%description libgbm-devel
%{Summary}.

%package libglapi
Summary:        Mesa shared glapi
Provides:       libglapi
Provides:       libglapi%{?_isa}
# If mesa-dri-drivers are installed, they must match in version. This is here to prevent using
# older mesa-dri-drivers together with a newer mesa-libglapi or its dependants.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2193135 .

%description libglapi
%{Summary}.

%prep
%autosetup -n mesa-qvp-23.2.0

%build
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"

# We've gotten a report that enabling LTO for mesa breaks some games. See
# https://bugzilla.redhat.com/show_bug.cgi?id=1862771 for details.
# Disable LTO for now
%define _lto_cflags %{nil}

echo 'with_opencl'
%meson \
  --prefix=/usr/qvp \
  --libdir=/usr/qvp/lib64 \
  --libexecdir=/usr/qvp/libexec --bindir=/usr/qvp/bin --sbindir=/usr/qvp/sbin --includedir=/usr/qvp/include --datadir=/usr/qvp/share --mandir=/usr/qvp/share/man --infodir=/usr/qvp/share/info --localedir=/usr/qvp/share/local \
  -D dri-drivers-path=/usr/qvp/lib64/dri\
  -Dplatforms=x11,wayland \
  -Ddri3=enabled \
  -Dosmesa=true \
%if 0%{?with_hardware}
  -Dgallium-drivers=swrast,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_kmsro:,kmsro}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink} \
%else
  -Dgallium-drivers=swrast,virgl \
%endif
  -Dgallium-drivers=swrast,virgl \
  -Dgallium-vdpau=disabled \
  -Dgallium-omx=%{?with_omx:bellagio}%{!?with_omx:disabled} \
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
  -Dgallium-xa=%{?with_xa:enabled}%{!?with_xa:disabled} \
  -Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
  -Dgallium-opencl=%{?with_opencl:disabled}%{!?with_opencl:disabled} \
  -Dgallium-rusticl=false \
  -Dglvnd=false \
%if 0%{?with_opencl}
  -Dgallium-rusticl=false \
%endif
  -Dvulkan-drivers=[] \
  -Dvulkan-layers=[] \
  -Dshared-glapi=enabled \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
%if 0%{?with_intel_clc}
  -Dintel-clc=enabled \
%endif
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Dbuild-tests=false \
  -Dselinux=true \
%if !0%{?with_libunwind}
  -Dlibunwind=disabled \
%endif
%if !0%{?with_lmsensors}
  -Dlmsensors=disabled \
%endif
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true
%endif
 %{nil}
%meson_build

# libvdpau opens the versioned name, don't bother including the unversioned
rm -vf %{buildroot}/usr/qvp/lib64/vdpau/*.so
# likewise glvnd
# We get those from libglvnd
rm -rf	%{buildroot}%{_includedir}/EGL/eglext.h \
	%{buildroot}%{_includedir}/EGL/egl.h \
	%{buildroot}%{_includedir}/EGL/eglplatform.h \
	%{buildroot}%{_includedir}/KHR \
	%{buildroot}%{_includedir}/GLES \
	%{buildroot}%{_includedir}/GLES2 \
	%{buildroot}%{_includedir}/GLES3 \
	%{buildroot}%{_includedir}/KHR/khrplatform.h \
	%{buildroot}%{_libdir}/pkgconfig/egl.pc \
	%{buildroot}%{_libdir}/pkgconfig/glesv2.pc \
	%{buildroot}%{_libdir}/libEGL.so.1 \
	%{buildroot}%{_libdir}/libEGL.so \
	%{buildroot}%{_libdir}/libGLESv1_CM.so.1 \
	%{buildroot}%{_libdir}/libGLESv1_CM.so \
	%{buildroot}%{_libdir}/libGLESv2.so

%install
%meson_install
# XXX can we just not build this

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
#ln -s /usr/qvp/lib64/libGLX_mesa.so.0 %{buildroot}/usr/qvp/lib64/libGLX_system.so.0

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{qvplibdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
rm -rf  %{buildroot}%{_includedir}/EGL/eglext.h \
        %{buildroot}%{_includedir}/EGL/egl.h \
        %{buildroot}%{_includedir}/EGL/eglplatform.h \
        %{buildroot}%{_includedir}/KHR \
        %{buildroot}%{_includedir}/GLES \
        %{buildroot}%{_includedir}/GLES2 \
        %{buildroot}%{_includedir}/GLES3 \
        %{buildroot}%{_includedir}/KHR/khrplatform.h \
        %{buildroot}%{_libdir}/pkgconfig/egl.pc \
        %{buildroot}%{_libdir}/pkgconfig/glesv2.pc \
        %{buildroot}%{_libdir}/libEGL.so.1 \
        %{buildroot}%{_libdir}/libEGL.so \
        %{buildroot}%{_libdir}/libGLESv1_CM.so.1 \
        %{buildroot}%{_libdir}/libGLESv1_CM.so \
        %{buildroot}%{_libdir}/libGLESv2.so

popd

%files filesystem
%dir %{qvplibdir}/dri

%files libGL
%files libGL-devel
%dir %{qvpincludedir}/GL
%dir %{qvpincludedir}/GL/internal
%dir %{qvplibdir}/pkgconfig
%{qvpincludedir}/GL/internal/dri_interface.h
%{qvplibdir}/pkgconfig/dri.pc
%{qvplibdir}/libglapi.so

%files libEGL
%files libEGL-devel
%dir %{qvpincludedir}/EGL
%{qvpincludedir}/EGL/eglext_angle.h
%{qvpincludedir}/EGL/eglmesaext.h
%{qvpincludedir}/EGL/egl.h
%{qvpincludedir}/EGL/eglext.h
%{qvpincludedir}/EGL/eglplatform.h

%files libglapi
%{qvplibdir}/libglapi.so.0
%{qvplibdir}/libglapi.so.0.*

%files libOSMesa
%{qvplibdir}/libOSMesa.so.8*
%{qvplibdir}/libEGL.so
%{qvplibdir}/libEGL.so.1
%{qvplibdir}/libEGL.so.1.0.0
%{qvplibdir}/libGL.so
%{qvplibdir}/libGL.so.1
%{qvplibdir}/libGL.so.1.2.0
%{qvplibdir}/libGLESv1_CM.so
%{qvplibdir}/libGLESv1_CM.so.1
%{qvplibdir}/libGLESv1_CM.so.1.1.0
%{qvplibdir}/libGLESv2.so
%{qvplibdir}/libGLESv2.so.2
%{qvplibdir}/libGLESv2.so.2.0.0
%{qvplibdir}/pkgconfig/egl.pc
%{qvplibdir}/pkgconfig/gl.pc
%{qvplibdir}/pkgconfig/glesv1_cm.pc
%{qvplibdir}/pkgconfig/glesv2.pc
%files libOSMesa-devel
%dir %{qvpincludedir}/GL
%dir %{qvpincludedir}/GLES
%dir %{qvpincludedir}/GLES2
%dir %{qvpincludedir}/GLES3
%{qvpincludedir}/GL/osmesa.h
%{qvpincludedir}/GL/gl.h
%{qvpincludedir}/GL/glcorearb.h
%{qvpincludedir}/GL/glext.h
%{qvpincludedir}/GL/glx.h
%{qvpincludedir}/GL/glxext.h
%{qvpincludedir}/GLES/egl.h
%{qvpincludedir}/GLES/gl.h
%{qvpincludedir}/GLES/glext.h
%{qvpincludedir}/GLES/glplatform.h
%{qvpincludedir}/GLES2/gl2.h
%{qvpincludedir}/GLES2/gl2ext.h
%{qvpincludedir}/GLES2/gl2platform.h
%{qvpincludedir}/GLES3/gl3.h
%{qvpincludedir}/GLES3/gl31.h
%{qvpincludedir}/GLES3/gl32.h
%{qvpincludedir}/GLES3/gl3ext.h
%{qvpincludedir}/GLES3/gl3platform.h
%{qvpincludedir}/KHR/khrplatform.h
%{qvplibdir}/libOSMesa.so
%{qvplibdir}/pkgconfig/osmesa.pc

%files libgbm
%{qvplibdir}/libgbm.so.1
%{qvplibdir}/libgbm.so.1.*
%files libgbm-devel
%{qvplibdir}/libgbm.so
%{qvpincludedir}/gbm.h
%{qvplibdir}/pkgconfig/gbm.pc

%files dri-drivers
%dir %{qvpdatadir}/drirc.d
%dir %{qvplibdir}/dri
%{qvpdatadir}/drirc.d/00-mesa-defaults.conf
%{qvplibdir}/dri/kms_swrast_dri.so
%{qvplibdir}/dri/swrast_dri.so
%{qvplibdir}/dri/virtio_gpu_dri.so

%if 0%{?with_hardware}
%if 0%{?with_r300}
%{qvplibdir}/dri/r300_dri.so
%endif
%if 0%{?with_radeonsi}
%if 0%{?with_r600}
%{qvplibdir}/dri/r600_dri.so
%endif
%{qvplibdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64
%{qvplibdir}/dri/crocus_dri.so
%{qvplibdir}/dri/i915_dri.so
%{qvplibdir}/dri/iris_dri.so
%endif
%ifarch aarch64 x86_64 %{ix86}
%{qvplibdir}/dri/ingenic-drm_dri.so
%{qvplibdir}/dri/imx-drm_dri.so
%{qvplibdir}/dri/imx-lcdif_dri.so
%{qvplibdir}/dri/kirin_dri.so
%{qvplibdir}/dri/komeda_dri.so
%{qvplibdir}/dri/mali-dp_dri.so
%{qvplibdir}/dri/mcde_dri.so
%{qvplibdir}/dri/mxsfb-drm_dri.so
%{qvplibdir}/dri/rcar-du_dri.so
%{qvplibdir}/dri/stm_dri.so
%endif
%if 0%{?with_vc4}
%{qvplibdir}/dri/vc4_dri.so
%endif
%if 0%{?with_v3d}
%{qvplibdir}/dri/v3d_dri.so
%endif
%if 0%{?with_freedreno}
%{qvplibdir}/dri/kgsl_dri.so
%{qvplibdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{qvplibdir}/dri/etnaviv_dri.so
%endif
%if 0%{?with_tegra}
%{qvplibdir}/dri/tegra_dri.so
%endif
%if 0%{?with_lima}
%{qvplibdir}/dri/lima_dri.so
%endif
%if 0%{?with_panfrost}
%{qvplibdir}/dri/panfrost_dri.so
%endif
%{qvplibdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{qvplibdir}/dri/vmwgfx_dri.so
%endif
%if 0%{?with_kmsro}
%{qvplibdir}/dri/armada-drm_dri.so
%{qvplibdir}/dri/exynos_dri.so
%{qvplibdir}/dri/hdlcd_dri.so
%{qvplibdir}/dri/hx8357d_dri.so
%{qvplibdir}/dri/ili9225_dri.so
%{qvplibdir}/dri/ili9341_dri.so
%{qvplibdir}/dri/imx-dcss_dri.so
%{qvplibdir}/dri/mediatek_dri.so
%{qvplibdir}/dri/meson_dri.so
%{qvplibdir}/dri/mi0283qt_dri.so
%{qvplibdir}/dri/pl111_dri.so
%{qvplibdir}/dri/repaper_dri.so
%{qvplibdir}/dri/rockchip_dri.so
%{qvplibdir}/dri/st7586_dri.so
%{qvplibdir}/dri/st7735r_dri.so
%{qvplibdir}/dri/sun4i-drm_dri.so
%endif
%endif

%if 0%{?with_va}
%{qvplibdir}/dri/virtio_gpu_drv_video.so
%endif

%files
%if 0%{?with_vulkan_hw}
%{qvplibdir}/libvulkan_radeon.so
%{qvpdatadir}/drirc.d/00-radv-defaults.conf
%{qvpdatadir}/vulkan/icd.d/radeon_icd.*.json
%{qvplibdir}/libvulkan_intel.so
%{qvpdatadir}/vulkan/icd.d/intel_icd.*.json
%{qvplibdir}/libvulkan_intel_hasvk.so
%{qvpdatadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%{qvplibdir}/libvulkan_broadcom.so
%{qvpdatadir}/vulkan/icd.d/broadcom_icd.*.json
%{qvplibdir}/libvulkan_freedreno.so
%{qvpdatadir}/vulkan/icd.d/freedreno_icd.*.json
%{qvplibdir}/libvulkan_panfrost.so
%{qvpdatadir}/vulkan/icd.d/panfrost_icd.*.json
%endif
