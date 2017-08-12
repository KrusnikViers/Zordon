from app.models.base import SubscriptionBase as _Base, DefferedSubscription as _Deffered


class Subscription(_Base):
    pass


_Deffered.set_model(Subscription)
