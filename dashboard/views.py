from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from sales.models import Sale
from payments.models import Payment, Refund


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    permission_required = ['dashboard:view_dashboard']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        last_7_days = timezone.now() - timedelta(days=7)

        # SALES
        sales_today = Sale.objects.filter(
            created_at__date=today,
            status=Sale.COMPLETED
        )

        total_sales_today = sales_today.count()

        gross_revenue = Sale.objects.filter(
            status=Sale.COMPLETED
        ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")

        completed_sales_count = Sale.objects.filter(
            status=Sale.COMPLETED
        ).count()

        draft_sales_count = Sale.objects.filter(
            status=Sale.DRAFT
        ).count()

        voided_sales_count = Sale.objects.filter(
            status=Sale.VOIDED
        ).count()

        refunded_sales_count = Sale.objects.filter(
            status=Sale.REFUNDED
        ).count()

        # PAYMENTS
        total_payments = Payment.objects.filter(
            status="completed"
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        pending_payments = Payment.objects.filter(
            status="pending"
        ).count()

        # Payments by method
        payments_by_method = Payment.objects.filter(
            status="completed"
        ).values("method__name").annotate(
            total=Sum("amount")
        )

        # REFUNDS
        total_refunds = Refund.objects.filter(
            status="completed"
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        refund_count = Refund.objects.filter(
            status="completed"
        ).count()

        # NET REVENUE
        net_revenue = gross_revenue - total_refunds

        refund_rate = (
            (total_refunds / gross_revenue) * 100
            if gross_revenue > 0 else 0
        )

 
        # Last 7 Days Revenue
        last_7_sales = Sale.objects.filter(
            status=Sale.COMPLETED,
            created_at__gte=last_7_days
        )

        last_7_revenue = last_7_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0.00")

        context.update({
            "total_sales_today": total_sales_today,
            "gross_revenue": gross_revenue,
            "total_payments": total_payments,
            "total_refunds": total_refunds,
            "net_revenue": net_revenue,
            "refund_rate": round(refund_rate, 2),

            "completed_sales_count": completed_sales_count,
            "draft_sales_count": draft_sales_count,
            "voided_sales_count": voided_sales_count,
            "refunded_sales_count": refunded_sales_count,

            "pending_payments": pending_payments,
            "payments_by_method": payments_by_method,
            "refund_count": refund_count,
            "last_7_revenue": last_7_revenue,
        })

        return context
